from typing import Union
import json
from .pd_models import UserData, UserQuiz,UserIdQuizes
import csv
from typing import List, Union, Set

from db.models import Results, Quiz, UserRedisRow


EXP_HOURS = 60 * 60 * 48


class RedisCrud:
    def __init__(self, db):
        self.db = db

    async def get_user(self, user_id: int) -> Union[UserData, None]:
        user = await self.db.get(user_id)
        if user is None:
            return None
        user = json.loads(user)
        return user

    async def set_user(self, quiz_id: int, user_id: int, user_data: UserQuiz) :
        user = await self.get_user(user_id=user_id)
        if user is None:
            user = {'quizes': {}}
        user_data = user_data.dict()
        user['quizes'][quiz_id] = user_data.get('questions')
        data = json.dumps(user)
        await self.db.set(user_id, data, EXP_HOURS)

    async def export_user_results(self, user_id: int) -> Union[str, None]:
        result = await self.get_user(user_id=user_id)
        if result is None:
            return None
        quizes = result.get('quizes')
        answers = []
        for quiz in quizes.keys():
            for question in quizes.get(quiz):
                answers.append([quiz, question.get('question_id'), question.get('answer_id')])

        headers = ['quiz_id', 'question_id', 'answer_id']
        filename = f'user_{user_id}.csv'
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(answers)
            return filename

    async def export_users_results(self, results: List[Results], company_id: int)  -> str:
        headers = ['user_id', 'quiz_id', 'question_id', 'answer_id']
        users_id = set([result.user_id for result in results])
        filename = f'company_{company_id}'

        users_rows = await self.iterate_users(users_id=users_id)

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            writer.writerows(users_rows)
        return filename

    async def iterate_users(self, users_id: Set[int]) -> List[UserRedisRow]:
        users_data = []
        for id in users_id:
            user = await self.get_user(user_id=id)

            user['id'] = id
            data = UserIdQuizes(id=user.get('id'), quizes=user.get('quizes'))
            users_data.append(data)

        users_rows = []
        for user in users_data:
            quizes = user.quizes
            for quiz in quizes:
                for question in quiz.questions:
                    user_row = UserRedisRow(id=user.id,
                                    quiz_id=quiz.quiz_id,
                                    question_id=question.question_id,
                                    answer_id=question.answer_id
                                            )

                    users_rows.append(user_row)

        return users_rows