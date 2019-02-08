#!/Python27/python.exe -u

import cgi
import sys
import traceback
import cgitb
cgitb.enable()



form=cgi.FieldStorage()
ccname=form.getvalue("ccname","0")
pno=form.getvalue("pno","0")
sdate=form.getvalue("sdate","0")
edate=form.getvalue("edate","0")
eType=form.getvalue("eType","0")
epno=form.getvalue("epno","0")

print "Content-type: text/html"
print
print "<html><head>"
print "<title>Royal Palace | Create Reservation</title>"
print "</head><body background='https://img.clipartfox.com/6a29a43166d4497e459f338554225e82_floral-frame-with-brown-light-brown-background-clipart_1024-731.jpeg'>"
print "<a href='./AddCustomer.html'>Home</a><br/><br/>"


"""following modules are needed to connnect 
to MySQL database and run a query"""

import mysql.connector as connector
from mysql.connector import Error
import sys

#returns the connection for the provided DB info.
def db_connect(_host, _db, _user, _password):
    try:
        connection = connector.connect(host=_host, database=_db, user=_user, password=_password)
        #print 'Connection to '+_db+' for '+_user+' is successful'


        return connection
    except Error as e:
        print(e)
        return NULL

#returns the cursor for the provided query executed on the provided connection
def execute_query(connection, query):

    """
    1- try ... except" is used to deal with situations where unexpected events may occur
    2- instructions for the expected behavior goes into "try-block"
    3- instructions for unexpected behavior goes into "except-bloack"
    4- finally-block" has the instruction that must run in both the situations, expected and unexpected
    """
    try:
        #obtain curor on the given connection for db
        cursor = connection.cursor()

        # execute the query through the curson on given connectino
        cursor.execute(query)
        hd = [i[0] for i in cursor.description]
        rows = [list(i) for i in cursor.fetchall()]
        rows.insert(0,hd)
    #rows = [list(i) for i in cursor.fetchall()]
        
        #rows=[list(i) for i in cur.fetchall()]
        #head = [i[0] for i in cursor.description]
        #head = cursor.description()
        #rows = [list(i) for i in cursor.fetchall()]
        #header=[i[0] for i in cursor.description]
        #rows = cursor.fetchall()
        #header=cursor.description
        
        #rows.insert(0,header)

        #prints total number of results (rows)
        #print('Total Row(s):', cursor.rowcount)

        #iterate over all the rows
        #for row in rows:
            #print all values in row
        #    print(row)


        return rows
    except Error as e:
        print e
        """
        since error has occured, rollback the changes 
        that were made by the execution of the query
        """
        connection.rollback()
    finally:
        #close the connection with cursor
        cursor.close()




if __name__ == '__main__':

    #sys.argv is a list that has argumnets given to the program at run time


    #we use the following function to connect to database
    connection = db_connect('localhost', 'sonifinal','root','Rooney@10')
    cursor = connection.cursor()

        # execute the query through the curson on given connectino
    cursor.execute("Select EventID from Events where EventName='"+eType+"'")
    event_result=cursor.fetchone();

    insert_query="INSERT INTO `sonifinal`.`eventreservation`(`VisitorName`,`ContactNo`,'EventId','NoOfGuest',`StartDate`,`EndDate`)"
    #insert_query+="VALUES('"+ccname+"','"+pno+"','"+eType+"','"+epno+"','"+sdate+"','"+edate+"')";
    insert_query+="VALUES('"+ccname+"',"+pno+",'"(event_result[0])+"',"+epno+",,'"+sdate+"','"+edate+"')";
    
    cursor.execute(insert_query)
    connection.commit()
    print "<h1> A New Event was added to the table</h1>"
    connection.close();

print "</body></html>"