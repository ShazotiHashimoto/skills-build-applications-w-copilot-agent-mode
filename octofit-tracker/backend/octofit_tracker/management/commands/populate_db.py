from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index({'email': 1}, unique=True)

        # Sample data
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
        ]
        teams = [
            {'name': 'Marvel', 'members': ['spiderman@marvel.com', 'ironman@marvel.com']},
            {'name': 'DC', 'members': ['wonderwoman@dc.com', 'batman@dc.com']},
        ]
        activities = [
            {'user_email': 'spiderman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'ironman@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'wonderwoman@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user_email': 'batman@dc.com', 'activity': 'Yoga', 'duration': 20},
        ]
        leaderboard = [
            {'team': 'Marvel', 'points': 75},
            {'team': 'DC', 'points': 80},
        ]
        workouts = [
            {'user_email': 'spiderman@marvel.com', 'workout': 'HIIT', 'suggestion': 'Try 20 min HIIT'},
            {'user_email': 'ironman@marvel.com', 'workout': 'Strength', 'suggestion': 'Bench press 3x10'},
            {'user_email': 'wonderwoman@dc.com', 'workout': 'Cardio', 'suggestion': 'Run 5km'},
            {'user_email': 'batman@dc.com', 'workout': 'Flexibility', 'suggestion': 'Stretch for 15 min'},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
