from datetime import datetime

dt1 = datetime.strptime("Wednesday, October 2, 2002", "%A, %B %d, %Y")
dt2 = datetime.strptime("Friday, 11.10.13", "%A, %d.%m.%y")
dt3 = datetime.strptime("Thursday, 18 August 1977", "%A, %d %B %Y")