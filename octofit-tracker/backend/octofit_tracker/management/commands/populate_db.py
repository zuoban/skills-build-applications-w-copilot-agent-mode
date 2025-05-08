from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_users, test_teams, test_activities, test_leaderboard, test_workouts
from bson import ObjectId
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data for users, teams, activities, leaderboard, and workouts.'

    def handle(self, *args, **kwargs):
        # 清空所有集合
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # 创建用户
        user_objs = []
        for u in test_users:
            user = User(_id=u['_id'], username=u['username'], email=u['email'], password=u['password'])
            user.save()
            user_objs.append(user)

        # 填充团队成员
        for t in test_teams:
            t['members'] = user_objs

        # 创建团队
        team_objs = []
        for t in test_teams:
            team = Team(_id=t['_id'], name=t['name'])
            team.save()
            for member in t['members']:
                team.members.add(member)
            team_objs.append(team)

        # 关联活动和排行榜用户
        for idx, a in enumerate(test_activities):
            a['user'] = user_objs[idx]
        for idx, l in enumerate(test_leaderboard):
            l['user'] = user_objs[idx]

        # 创建活动
        for a in test_activities:
            Activity(_id=a['_id'], user=a['user'], activity_type=a['activity_type'], duration=a['duration']).save()

        # 创建排行榜
        for l in test_leaderboard:
            Leaderboard(_id=l['_id'], user=l['user'], score=l['score']).save()

        # 创建锻炼
        for w in test_workouts:
            Workout(_id=w['_id'], name=w['name'], description=w['description']).save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the octofit_db database with test data.'))
