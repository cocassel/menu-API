from flask import Flask, jsonify, url_for, request, redirect
from flask_cors import CORS
from collections import OrderedDict
from flask import request
import psycopg2
from threading import Thread, Lock


app= Flask(__name__)
CORS(app)
lock = Lock()


def connectToDB():
    try:  # attempts to connect to the database
        con = psycopg2.connect("dbname='pxeebvqz' user='pxeebvqz' "
                               "host='nutty-custard-apple.db.elephantsql.com' "
                               "port='5432' password='uHbUVNzUAjDS7CJmv7gmFTxz-_FuHbRX'")
        print("Connected")
    except:
        print("I am unable to connect to the database")
    cur = con.cursor()
    return cur, con


def getMenuDishes():
    try:
        cur, con = connectToDB()
        cur.execute("select * from public.menu_dish")
        menuTable = cur.fetchall()
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='menu_dish'")
        columnNames = cur.fetchall()

        menuList = []

        for tuple in range(menuTable.__len__()):
            menuDict = OrderedDict()
            for column in range(columnNames.__len__()):
                key = columnNames[column][0]
                value = str(menuTable[tuple][column])
                if value == "None":
                    value = ""
                menuDict[key] = value
            menuDict["visible"]= "true"
            menuList.append(menuDict)

        return menuList
    except:
        print("Menu could not be retrieved from the database")
    finally:
        con.close()


def getDishTypes():
    try:
        cur, con = connectToDB()
        cur.execute("select * from public.dish_type")
        table = cur.fetchall()
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='dish_type'")
        columnNames = cur.fetchall()

        tableList = []

        for tuple in range(table.__len__()):
            tableDict = OrderedDict()
            for column in range(columnNames.__len__()):
                key = columnNames[column][0]
                value = str(table[tuple][column])
                if value == "None":
                    value = ""
                tableDict[key] = value
            tableList.append(tableDict)

        return tableList
    except:
        print("Dish types could not be retrieved from the database")
    finally:
        con.close()


def getFlags():
    try:
        cur, con = connectToDB()
        cur.execute("select * from public.dietary_flag")
        table = cur.fetchall()
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='dietary_flag'")
        columnNames = cur.fetchall()

        tableList = []

        for tuple in range(table.__len__()):
            tableDict = OrderedDict()
            for column in range(columnNames.__len__()):
                key = columnNames[column][0]
                value = str(table[tuple][column])
                if (value == "None"):
                    value = ""
                tableDict[key] = value
            tableDict["selected"] = False
            tableList.append(tableDict)

        return tableList
    except:
        print("Flags types could not be retrieved from the database")
    finally:
        con.close()


def getFlaggedDishes():
    try:
        cur, con = connectToDB()
        cur.execute("select * from public.flagged_menu_dish")
        table = cur.fetchall()
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='flagged_menu_dish'")
        columnNames = cur.fetchall()

        tableList = []

        for tuple in range(table.__len__()):
            tableDict = OrderedDict()
            for column in range(columnNames.__len__()):
                key = columnNames[column][0]
                value = str(table[tuple][column])
                if (value == "None"):
                    value = ""
                tableDict[key] = value
            tableList.append(tableDict)

        return tableList
    except:
        print("Flagged dishes could not be retrieved from the database")
    finally:
        con.close()


def authenticateUserFromDb(username, password):
    try:
        cur, con = connectToDB()
        cur.execute("select * from public.user")
        userTable = cur.fetchall()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='user'")

        for tuple in range(userTable.__len__()):
            userTuple = userTable[tuple]
            if userTuple[1] == username and userTuple[2] == password:
                if userTuple[5] == True:
                    return jsonify({"user": "authenticated", "id": userTuple[0]}), 200
                return jsonify({"user": "authenticated", "id": "invalid"}), 200
        return jsonify({"user": "denied"}), 200
    except:
        print("User could not be authenticated")
    finally:
        con.close()


def getUsers():
    try:
        cur, con = connectToDB()
        cur.execute("select * from public.user")
        userTable = cur.fetchall()
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='user'")
        columnNames = cur.fetchall()

        userList = []

        for tuple in range(userTable.__len__()):
            userDict = OrderedDict()
            for column in range(columnNames.__len__()):
                key = columnNames[column][0]
                value = str(userTable[tuple][column])
                if (value == "None"):
                    value = ""
                userDict[key] = value
            userList.append(userDict)

        return userList
    except:
        print("Users could not be retrieved from the database")
    finally:
        con.close()


def addUserToDB(userToAdd):
    try:
        cur, con = connectToDB()

        getUserID = "select count(*) from public.user"
        cur.execute(getUserID)
        newUserID = cur.fetchall()[0][0]
        newUserID = newUserID + 1

        first_name = str(userToAdd["first_name"])
        first_name = first_name.replace("'", "''")
        last_name = str(userToAdd["last_name"])
        last_name = last_name.replace("'", "''")
        username = str(userToAdd["username"])
        username = username.replace("'", "''")
        password = str(userToAdd["password"])
        password = password.replace("'", "''")
        can_edit_users = str(userToAdd["can_edit_users"])

        insertStatement = "INSERT INTO public.user(user_id, username, password, first_name, last_name, can_edit_users) VALUES ('" + str(
            newUserID) + "', '" + username + "', '" + password+ "', '" + first_name + "','" + last_name  + "','" + can_edit_users + "')"
        print("User " + str(newUserID) + " has been added to the database")

        cur.execute(insertStatement)
        con.commit()
        con.close()
    except Exception as e:
        print(e.message)
        print("Could not add user to the database")
    finally:
        con.close()


def deleteUserFromDB(user):
  try:
    cur, con = connectToDB()
    deleteStatement="DELETE FROM public.user WHERE user_id=" + str(user)
    updateStatement="UPDATE public.user SET user_id=user_id-1 WHERE user_id>" + str(user)
    print("User " + str(user) + " has been deleted")
    cur.execute(deleteStatement)
    cur.execute(updateStatement)
    con.commit()
  except:
    print("Could not delete user from database")
  finally:
    con.close()


def addFlagToDB(flagToAdd):
    try:
        cur, con = connectToDB()

        getFlagID = "select count(*) from public.dietary_flag"
        cur.execute(getFlagID)
        newFlagID = cur.fetchall()[0][0]
        newFlagID = newFlagID + 1

        flag_name = str(flagToAdd["flag_name"])

        insertStatement = "INSERT INTO public.dietary_flag(flag_id, flag_name) VALUES ('" + str(newFlagID) + "', '" + flag_name + "')"

        cur.execute(insertStatement)
        con.commit()
        con.close()
    except Exception as e:
        print(e.message)
        print("Could not add flag to the database")
    finally:
        con.close()


def deleteFlagFromDB(flag):
  try:
    cur, con = connectToDB()
    deleteStatement="DELETE FROM public.dietary_flag WHERE flag_id=" + str(flag)
    updateStatement="UPDATE public.dietary_flag SET flag_id=flag_id-1 WHERE flag_id>" + str(flag)
    print("Flag " + str(flag) + " has been deleted")
    cur.execute(deleteStatement)
    cur.execute(updateStatement)
    con.commit()
  except:
    print("Could not delete flag from database")
  finally:
    con.close()


def updateFlagInDB(flagToUpdate):
    try:
        cur, con = connectToDB()

        flag_id = str(flagToUpdate['flag_id'])
        flag_name = str(flagToUpdate['flag_name'])

        updateStatement = "UPDATE public.dietary_flag SET flag_name='" + flag_name + "' WHERE flag_id=" + flag_id

        cur.execute(updateStatement)
        con.commit()
        con.close()
    except Exception as e:
        print(e.message)
        print("Could not update flag in the database")
    finally:
        con.close()


@app.route("/wakeup", methods=['GET'])
def wakeup():
    print("Waking up Heroku API")
    try:
        return jsonify({"Heroku": "Awake"}), 200
    except:
        print("Users could not be fetched")


@app.route("/dishes", methods=['GET'])
def dishes():
    lock.acquire()
    print("Calling menu")
    print("Menu now has the lock")
    try:
        
        return jsonify(getMenuDishes()), 200
    except:
        print("Menu could not be fetched")
    finally:
        print("Menu has released the lock")
        lock.release()


@app.route("/types", methods=['GET'])
def types():
    lock.acquire()
    print("Calling dish types")
    print("Dish types now has the lock")
    try:
        return jsonify(getDishTypes()), 200
    except:
        print("Dish types could not be fetched")
    finally:
        print("Dish types has released the lock")
        lock.release()


@app.route("/flags", methods=['GET'])
def flags():
    lock.acquire()
    print("Calling flags")
    print("Flags types now has the lock")
    try:
        return jsonify(getFlags()), 200
    except:
        print("Flags could not be fetched")
    finally:
        print("Flags has released the lock")
        lock.release()


@app.route("/flaggedDishes", methods=['GET'])
def flaggedDishes():
    lock.acquire()
    print("Calling flagged dishes")
    print("Flagged dishes now has the lock")
    try:
        return jsonify(getFlaggedDishes()), 200
    except:
        print("Flagged dishes could not be fetched")
    finally:
        print("Flagged dishes has released the lock")
        lock.release()


@app.route("/authenticateUser", methods=['POST'])
def authenticateAdminUser():
    lock.acquire()
    print("Calling authenticateAdminUser")
    print("authenticateAdminUser now has the lock")
    try:
        userToAuthenticate = request.json
        username = str(userToAuthenticate["username"])
        password = str(userToAuthenticate["password"])
        return authenticateUserFromDb(username, password)
    except Exception as e:
        print(e.message)
        print("Unable to authenticate user")
    finally:
        print("authenticateUser has released the lock")
        lock.release()


@app.route("/users", methods=['GET'])
def users():
    lock.acquire()
    print("Calling users")
    print("Users now has the lock")
    try:
        return jsonify(getUsers()), 200
    except:
        print("Users could not be fetched")
    finally:
        print("Users has released the lock")
        lock.release()


@app.route("/addUser", methods=['POST'])
def addUser():
    lock.acquire()
    print("Calling addUser")
    print("AddUser now has the lock")
    try:
        userToAdd = request.json
        addUserToDB(userToAdd)
        return jsonify({"addUser": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not add user")
        return jsonify({"addUser": "failed"})
    finally:
        print("AddUser has released the lock")
        lock.release()
	

@app.route("/addCategory", methods=['POST'])
def addCategory():
    lock.acquire()
    print("Calling addCategory")
    print("AddCategory now has the lock")
    try:
        categoryToAdd = request.json
        addCategoryToDB(categoryToAdd)
        return jsonify({"addCategory": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not add user")
        return jsonify({"addCategory": "failed"})
    finally:
        print("AddCategory has released the lock")
        lock.release()


@app.route("/addDish", methods=['POST'])
def addDish():
    lock.acquire()
    print("Calling addDish")
    print("AddCategory now has the lock")
    try:
        categoryToAdd = request.json
        addCategoryToDB(categoryToAdd)
        return jsonify({"addCategory": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not add user")
        return jsonify({"addCategory": "failed"})
    finally:
        print("AddCategory has released the lock")
        lock.release()


@app.route("/addFlag", methods=['POST'])
def addFlag():
    lock.acquire()
    print("Calling addFlag")
    print("AddFlag now has the lock")
    try:
        flagToAdd = request.json
        addFlagToDB(flagToAdd)
        return jsonify({"addFlag": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not add flag")
        return jsonify({"addFlag": "failed"})
    finally:
        print("AddFlag has released the lock")
        lock.release()


@app.route("/deleteDish", methods=['POST'])
def deleteDish():
    lock.acquire()
    print("Calling deleteDish")
    print("DeleteDish now has the lock")
    try:
        dishToDelete = request.json
        deleteDishFromDB(dishToDelete)
        return jsonify({"deleteDish": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not delete dish")
        return jsonify({"deleteDish": "failed"})
    finally:
        print("DeleteDish has released the lock")
        lock.release()


@app.route("/deleteUser", methods=['POST'])
def deleteUser():
    lock.acquire()
    print("Calling deleteUser")
    print("DeleteUser now has the lock")
    try:
        data = request.json
        userToDelete = data['deleteUser']
        deleteUserFromDB(userToDelete)
        return jsonify({"deleteUser": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not delete user")
        return jsonify({"deleteUser": "failed"})
    finally:
        print("DeleteUser has released the lock")
        lock.release()


@app.route("/deleteFlag", methods=['POST'])
def deleteFlag():
    lock.acquire()
    print("Calling deleteFlag")
    print("DeleteFlag now has the lock")
    try:
        data = request.json
        flagToDelete = data['deleteFlag']
        deleteFlagFromDB(flagToDelete)
        return jsonify({"deleteFlag": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not delete flag")
        return jsonify({"deleteFlag": "failed"})
    finally:
        print("DeleteFlag has released the lock")
        lock.release()


@app.route("/updateFlag", methods=['POST'])
def updateFlag():
    lock.acquire()
    print("Calling updateFlag")
    print("UpdateFlag now has the lock")
    try:
        flagToUpdate = request.json
        updateFlagInDB(flagToUpdate)
        return jsonify({"updateFlag": "success"}), 200
    except Exception as e:
        print(e.message)
        print("Could not update flag")
        return jsonify({"updateFlag": "failed"})
    finally:
        print("UpdateFlag has released the lock")
        lock.release()