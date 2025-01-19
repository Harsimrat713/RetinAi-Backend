import mysql.connector
from .sql_config import config
import re


def insertSessionsQuery(sessionID, data):
    leftChosen = ""
    rightChosen = ""
    for image in data["chosen_Images"]:
        match = re.search(r"(left|right)", image)
        if match:
            side = match.group(1)
            if side == "left":
                leftChosen = image
            elif side == "right":
                rightChosen = image

    query = f"""
      INSERT INTO sessions (sessionID, kioskID, imageLocation, chosenImageLeft, chosenImageRight) 
      VALUES ("{sessionID}", "{data["kiosk_id"]}", "{data["image_Paths"][0]}", "{leftChosen}", "{rightChosen}");
    """
    return query

def insertImagesQuery(sessionID, image_Info):
    # can have null if invalid images
    eyeSide = "null" if not image_Info['eyeSide'] else image_Info['eyeSide']
    prediction = "null" if not image_Info['prediction'] else image_Info['prediction']

    query = f"""
        INSERT INTO images (imageName, sessionID, eyeSide, cropped, prediction, selectedForDisp)
        VALUES ("{image_Info['name']}", "{sessionID}", "{eyeSide}", {image_Info['cropped']}, "{prediction}", {image_Info['selectedForDisp']});
    """
    return query


def info_Save(sessionID, data):
    try:
        # Establish a connection
        connection = mysql.connector.connect(**config)
        print("Connection successful!")

        if connection.is_connected():
            # Create a cursor object
            cursor = connection.cursor()
            fullQuery = ""
            
            # specifier for table
            tableSpecifier = "USE testCapstone;"

            # get insert query for session info
            sessionsQuery = insertSessionsQuery(sessionID, data)
            fullQuery = tableSpecifier + sessionsQuery

            # get insert query for image info
            for image in data['image_Info']:
                imageQuery = insertImagesQuery(sessionID, image)
                fullQuery = fullQuery + imageQuery

            # Execute full query
            for result in cursor.execute(fullQuery, multi=True):
                print(f"Result: {result.statement} - {result.rowcount} rows affected")


            # Fetch and print the results
            for table in cursor:
                print(table)
            # Commit the transaction
            connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# for testing
if __name__ == '__main__':
    sessionID = '01d4369b-f9db-41b7-bdba-39e9a10bcce1'
    data = {
        "kiosk_id": "asd",
        "image_Info": [
            {
            "name": "Corolla GR.jpg",
            "eyeSide": "",
            "cropped": False,
            "prediction": "",
            "selectedForDisp": False
            },
            {
            "name": "937_right.jpg",
            "eyeSide": "right",
            "cropped": True,
            "prediction": "Normal",
            "selectedForDisp": True
            },
            {
            "name": "937_left.jpg",
            "eyeSide": "left",
            "cropped": True,
            "prediction": "Normal",
            "selectedForDisp": True
            }
        ],
        "chosen_Images": [
            "937_right.jpg",
            "937_left.jpg"
        ],
        "image_Paths": [
            "images_store/01d4369b-f9db-41b7-bdba-39e9a10bcce1_Session_Images",
            "images_store/01d4369b-f9db-41b7-bdba-39e9a10bcce1_Session_Images/recieved_images",
            "images_store/01d4369b-f9db-41b7-bdba-39e9a10bcce1_Session_Images/cropped_images"
        ]
    }
    info_Save(sessionID, data)
