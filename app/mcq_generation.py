from typing import List
from nltk.tokenize import sent_tokenize
import toolz

from app.modules.duplicate_removal import remove_distractors_duplicate_with_correct_answer, remove_duplicates
from app.modules.text_cleaning import clean_text
from app.ml_models.answer_generation.answer_generator import AnswerGenerator
from app.ml_models.distractor_generation.distractor_generator import DistractorGenerator
from app.ml_models.question_generation.question_generator import QuestionGenerator
from app.ml_models.sense2vec_distractor_generation.sense2vec_generation import Sense2VecDistractorGeneration
from app.models.question import Question

import time
import random

class MCQGenerator():
    def __init__(self, is_verbose=False):
        start_time = time.perf_counter()
        print('Loading ML Models...')

        self.question_generator = QuestionGenerator()
        print('Loaded QuestionGenerator in', round(time.perf_counter() - start_time, 2), 'seconds.') if is_verbose else ''

        self.distractor_generator = DistractorGenerator()
        print('Loaded DistractorGenerator in', round(time.perf_counter() - start_time, 2), 'seconds.') if is_verbose else ''

        self.sense2vec_distractor_generator = Sense2VecDistractorGeneration()
        print('Loaded Sense2VecDistractorGenerator in', round(time.perf_counter() - start_time, 2), 'seconds.') if is_verbose else ''

    def generate_questions(self, context: str, mcq_count: int, id_count: int) -> List[Question]:
        cleaned_text = clean_text(context)
        desired_count = mcq_count + id_count
        all_questions = self._generate_question_answer_pairs(cleaned_text, desired_count)
        all_questions = self._generate_distractors(cleaned_text, all_questions)

        mcq_questions = []
        id_questions = []

        for question in all_questions:
            if len(question.distractors) >= 3 and len(mcq_questions) < mcq_count:
                mcq_questions.append(question)
            elif len(id_questions) < id_count:
                id_questions.append(question)
        
        remaining_questions = [question for question in all_questions if question not in mcq_questions + id_questions]

        for question in remaining_questions:
            if len(question.distractors) >= 3 and len(mcq_questions) < mcq_count:
                mcq_questions.append(question)
            elif len(id_questions) < id_count:
                id_questions.append(question)

        mcq_questions = self._generate_distractors(cleaned_text, mcq_questions)
        id_questions = self.generate_id_questions(id_questions)
        mcq_questions = self.generate_mcq_questions(mcq_questions, cleaned_text)
        return id_questions, mcq_questions


    def generate_id_questions(self, id_questions: List[Question]) -> List[Question]:
        for idx, question in enumerate(id_questions, start=1):
            print('-------------------')
            print(f"{idx}. ", question.questionText)
            print('Answer: ', question.answerText)
        return id_questions

    def generate_mcq_questions(self, mcq_questions: List[Question], cleaned_text: str) -> List[Question]:
        for idx, question in enumerate(mcq_questions, start=1):
            print('-------------------')
            print(f"{idx}. ", question.questionText)
            distractors = self._generate_distractors(cleaned_text, [question])[0].distractors
            full_choices = distractors[:4] + [question.answerText]
            random.shuffle(full_choices)
            choices = ['A', 'B', 'C', 'D']

            question.choices = full_choices
            question.correctChoice = choices[full_choices.index(question.answerText)]

            print('Choices:')
            for idx, choice in enumerate(full_choices[:4]):
                print(f"{choices[idx]}. {choice}")
            print('Answer: ', question.answerText)

        return mcq_questions


    def _generate_answers(self, context: str, desired_count: int) -> List[Question]:
        answers = self._generate_multiple_answers_according_to_desired_count(context, desired_count)

        print(answers)
        unique_answers = remove_duplicates(answers)

        questions = []
        for answer in unique_answers:
            questions.append(Question(answer))

        return questions

    def _generate_questions(self, context: str, questions: List[Question]) -> List[Question]:        
        for question in questions:
            question.questionText = self.question_generator.generate(question.answerText, context)

        return questions

    def _generate_question_answer_pairs(self, context: str, desired_count: int) -> List[Question]:
        context_splits = self._split_context_according_to_desired_count(context, desired_count)

        questions = []

        for split in context_splits:
            answer, question = self.question_generator.generate_qna(split)
            questions.append(Question(answer.capitalize(), question))

        questions = list(toolz.unique(questions, key=lambda x: x.answerText))

        return questions

    def _generate_distractors(self, context: str, questions: List[Question]) -> List[Question]:
        for question in questions:
            t5_distractors =  self.distractor_generator.generate(10, question.answerText, question.questionText, context)

            t5_distractors = remove_duplicates(t5_distractors)

            if len(t5_distractors) < 3:
                s2v_distractors = self.sense2vec_distractor_generator.generate(question.answerText, 3)
                distractors = t5_distractors + s2v_distractors
            else:
                distractors = t5_distractors


            distractors = remove_duplicates(distractors)
            distractors = remove_distractors_duplicate_with_correct_answer(question.answerText, distractors)

            question.distractors = distractors[:3]

        return questions

    def _generate_answer_for_each_sentence(self, context: str) -> List[str]:
        sents = sent_tokenize(context)

        answers = []
        for sent in sents:
            answers.append(self.answer_generator.generate(sent, 1)[0])

        return answers

    def _split_context_according_to_desired_count(self, context: str, desired_count: int) -> List[str]:
        sents = sent_tokenize(context)
        sent_count = len(sents)
        
        if sent_count <= desired_count:
            return sents
        
        context_splits = []
        take_sents_count = sent_count // desired_count
        start_sent_index = 0

        while start_sent_index < sent_count:
            context_split = ' '.join(sents[start_sent_index: start_sent_index + take_sents_count])
            context_splits.append(context_split)
            start_sent_index += take_sents_count

        if start_sent_index != sent_count:
            context_splits.append(' '.join(sents[start_sent_index:]))

        return context_splits

    
