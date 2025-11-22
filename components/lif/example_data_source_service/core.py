from typing import Dict, List


def users_info() -> dict:
    user = [
        {"id": "0001", "name": "User name 0001", "surname": "The surname 0001"},
        {"id": "1234", "name": "User name 1234", "surname": "The surname 1234"},
        {"id": "3456", "name": "User name 3456", "surname": "The surname 3456"},
    ]
    return {"user": user}


def users_info_filtered(filters: Dict = {}) -> List[Dict]:
    users = [
        {"id": 1000, "name": "Diego", "surname": "The surname 0001", "age": 30, "role": "student"},
        {"id": 1001, "name": "Diego", "surname": "The surname 0001", "age": 46, "role": "teacher"},
        {"id": 1002, "name": "Pepe", "surname": "The surname 0001", "age": 50, "role": "student"},
        {"id": 1003, "name": "User name 1234", "surname": "The surname 1234", "age": 30, "role": "student"},
        {"id": 1004, "name": "User name 3456", "surname": "The surname 3456", "age": 46, "role": "teacher"},
    ]
    return filter_users(users, filters)


def user_info(user_id) -> dict:
    user = [{"id": user_id, "name": "User name " + str(user_id), "surname": "The surname " + str(user_id)}]
    return {"user": user}


def courses_info(course_id) -> dict:
    courses = []
    if course_id:
        courses = [{"id": course_id, "name": "Course " + str(course_id), "code": "MAT101"}]
    else:
        courses = [
            {"name": "Course 1", "code": "MAT101"},
            {"name": "Course 2", "code": "HIS101"},
            {"name": "Course 3", "code": "COM101"},
        ]
    return {"courses": courses}


def filter_users(users: List[Dict], filters: Dict) -> List[Dict]:
    filtered_users = users
    if "role" in filters:
        filtered_users = [user for user in filtered_users if user.get("role") == filters["role"]]
    if "age_gt" in filters:
        filtered_users = [user for user in filtered_users if int(user.get("age", 0)) > filters["age_gt"]]
    if "age_lt" in filters:
        filtered_users = [user for user in filtered_users if int(user.get("age", 0)) < filters["age_lt"]]
    if "age" in filters:
        filtered_users = [user for user in filtered_users if int(user.get("age", 0)) == filters["age"]]
    if "name_like" in filters:
        filtered_users = [user for user in filtered_users if filters["name_like"] in user.get("name", "")]
    if "name" in filters:
        filtered_users = [user for user in filtered_users if user.get("name") == filters["name"]]
    return filtered_users
