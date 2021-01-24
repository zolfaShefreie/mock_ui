from .models import User, Class, Take, Teach
from .connect_to_auth import save_user_in_auth


def fill_user_table():
    result = save_user_in_auth("{\n    \"username\": \"stu1\",\n    \"password\": \"123pass\"\n}")
    user = User(id=int(result['ID']), username=result['username'], role="STUDENT")
    user.save()
    print(type(user.id))

    result = save_user_in_auth("{\n    \"username\": \"stu2\",\n    \"password\": \"123pass\"\n}")
    user2 = User(id=int(result['ID']), username=result['username'], role="STUDENT")
    user2.save()

    result = save_user_in_auth("{\n    \"username\": \"stu3\",\n    \"password\": \"123pass\"\n}")
    user3 = User(id=int(result['ID']), username=result['username'], role="STUDENT")
    user3.save()

    result = save_user_in_auth("{\n    \"username\": \"stu4\",\n    \"password\": \"123pass\"\n}")
    user4 = User(id=int(result['ID']), username=result['username'], role="STUDENT")
    user4.save()

    result = save_user_in_auth("{\n    \"username\": \"stu5\",\n    \"password\": \"123pass\"\n}")
    user5 = User(id=int(result['ID']), username=result['username'], role="STUDENT")
    user5.save()

    result = save_user_in_auth("{\n    \"username\": \"teacher1\",\n    \"password\": \"123pass\"\n}")
    user6 = User(id=int(result['ID']), username=result['username'], role="PROFESSOR")
    user6.save()

    result = save_user_in_auth("{\n    \"username\": \"teacher2\",\n    \"password\": \"123pass\"\n}")
    user7 = User(id=int(result['ID']), username=result['username'], role="PROFESSOR")
    user7.save()

    result = save_user_in_auth("{\n    \"username\": \"admin\",\n    \"password\": \"123pass\"\n}")
    user8 = User(id=int(result['ID']), username=result['username'], role="ADMIN")
    user8.save()


def fill_class_table():
    course = Class(id="123-1", name="course1")
    course.save()

    course2 = Class(id="123-2", name="course2")
    course2.save()


def fill_take_table():
    user = User.objects.get(username="stu1")
    take = Take(student=user, class_obj_id="123-1")
    take.save()

    user = User.objects.get(username="stu2")
    take2 = Take(student=user, class_obj_id="123-1")
    take2.save()

    user = User.objects.get(username="stu3")
    take3 = Take(student=user, class_obj_id="123-1")
    take3.save()

    user = User.objects.get(username="stu3")
    take4 = Take(student=user, class_obj_id="123-2")
    take4.save()

    user = User.objects.get(username="stu4")
    take5 = Take(student=user, class_obj_id="123-2")
    take5.save()

    user = User.objects.get(username="stu5")
    take6 = Take(student=user, class_obj_id="123-2")
    take6.save()


def fill_teach_table():
    user = User.objects.get(username="teacher1")
    teach = Teach(teacher=user, class_obj_id="123-1")
    teach.save()

    user = User.objects.get(username="teacher2")
    teach2 = Teach(teacher=user, class_obj_id="123-2")
    teach2.save()


def fill_database():
    fill_user_table()
    fill_class_table()
    fill_take_table()
    fill_teach_table()
