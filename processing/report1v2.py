#this file pulls the data required to build the MSA aggregate report 1 covering application dispositions
#rows are application disposition pulled from the action taken field
# 1) loan originated, 2)loan not accepted, 3) application denied, 4) applicatoin withdrawn, 5)incomplete, 6)loan purchased (for report 2)
class report_1_(object):
	def __init__(self):

		import psycopg2

		self.inputs = {}
        dbname = credentials[0]
        user = credentials[1]
        host = credentials[2]
        password = credentials[3]

        connect_string = "dbname=%s user=%s host=%s password=%s" % (dbname, user, host, password)
		#attempte a connection to the SQL database hosting the LAR information
		conn = psycopg2.connect("dbname='hmdamaster' user='roellk' host='localhost' password=''")
		self.conn = conn
		self.cur = conn.cursor()
		#this dictionary holds the data values needed to build tables 1 and 2
	#set the type by user filter in the controller object or fork and have 2 dictionaries
	#year and MSA information all need to be set in the controller object
		self.table_1 = {
		"action": {
			"originated": {
				"GS count": 0,
				"GS value": 0,
				"conventional count": 0,
				"conventional value": 0,
				"refinance count": 0,
				"refinance value": 0,
				"home improvement count": 0,
				"home improvement value": 0,
				"multifamily count": 0,
				"multifamily value": 0,
				"non-occupant count": 0,
				"non-occupant value": 0,
				"manufactured count": 0,
				"manufactured value": 0
		},
			"not accepted": {
				"GS count": 0,
				"GS value": 0,
				"conventional count": 0,
				"conventional value": 0,
				"refinance count": 0,
				"refinance value": 0,
				"home improvement count": 0,
				"home improvement value": 0,
				"multifamily count": 0,
				"multifamily value": 0,
				"non-occupant count": 0,
				"non-occupant value": 0,
				"manufactured count": 0,
				"manufactured value": 0
		},
			"denied": {
				"GS count": 0,
				"GS value": 0,
				"conventional count": 0,
				"conventional value": 0,
				"refinance count": 0,
				"refinance value": 0,
				"home improvement count": 0,
				"home improvement value": 0,
				"multifamily count": 0,
				"multifamily value": 0,
				"non-occupant count": 0,
				"non-occupant value": 0,
				"manufactured count": 0,
				"manufactured value": 0
		},
			"withdrawn": {
				"GS count": 0,
				"GS value": 0,
				"conventional count": 0,
				"conventional value": 0,
				"refinance count": 0,
				"refinance value": 0,
				"home improvement count": 0,
				"home improvement value": 0,
				"multifamily count": 0,
				"multifamily value": 0,
				"non-occupant count": 0,
				"non-occupant value": 0,
				"manufactured count": 0,
				"manufactured value": 0
		},
			"incomplete": {
				"GS count": 0,
				"GS value": 0,
				"conventional count": 0,
				"conventional value": 0,
				"refinance count": 0,
				"refinance value": 0,
				"home improvement count": 0,
				"home improvement value": 0,
				"multifamily count": 0,
				"multifamily value": 0,
				"non-occupant count": 0,
				"non-occupant value": 0,
				"manufactured count": 0,
				"manufactured value": 0
		},
			"purchased": {
				"GS count": 0,
				"GS value": 0,
				"conventional count": 0,
				"conventional value": 0,
				"refinance count": 0,
				"refinance value": 0,
				"home improvement count": 0,
				"home improvement value": 0,
				"multifamily count": 0,
				"multifamily value": 0,
				"non-occupant count": 0,
				"non-occupant value": 0,
				"manufactured count": 0,
				"manufactured value": 0
			}
			}
		}

	def parse_inputs(self, row):
			#splits the tuples into word variables for easy reading
		self.inputs['census_tract'] = row[0]
		self.inputs['loan_type'] = row[1]
		self.inputs['occupancy_status'] = row[2]
		self.inputs['loan_amount'] = row[3]
		self.inputs['action_type'] = row[4]
		self.inputs['loan_purpose'] = row[5]
		self.inputs['property_type'] = row[6]

	def table_1_aggregator(self, inputs):

		#convert action_type code to a word for inputting data into dictionary
		if inputs['action_type'] == '1':
			action = 'originated'
		elif inputs['action_type'] == '2':
			action = 'not accepted'
		elif inputs['action_type'] == '3':
			action = 'denied'
		elif inputs['action_type'] == '4':
			action = 'withdrawn'
		elif inputs['action_type'] == '5':
			action = 'incomplete'
		elif inputs['action_type'] == '6':
			action = 'purchased'

		#convert occupancy status to word for inputting into data dictionary
		if inputs['occupancy_status'] == '1':
			occupancy = 'owner occupied'
		elif inputs['occupancy_status'] == '2':
			occupancy = 'non-occupant'

		#convert loan_purpose to word for inputting into data dictionary
		if inputs['loan_purpose'] == '1':
			purpose = 'purchase'
		elif inputs['loan_purpose'] == '2':
			purpose = 'home improvement'
		elif inputs['loan_purpose'] =='3':
			purpose = 'refinance'

		#convert property type to word for inputting into data dictionary
		if inputs['property_type'] == '1':
			prop = '1-4 family' #excludes manufactured housing
		elif inputs['property_type'] == '2':
			prop = 'manufactured'
		elif inputs['property_type'] == '3':
			prop = 'multifamily'

		#convert loan type to word for inputting into data dictionary
		if inputs['loan_type'] == '1':
			loan = 'conventional'
		elif inputs['loan_type'] == '2' or inputs['loan_type'] == '3' or inputs['loan_type'] == '4':
			loan = 'GS'

		#concatenate the count and value strings to access the dictionary
		occupancy_count = occupancy + ' count'
		occupancy_value = occupancy + ' value'
		loan_type_count = loan + ' count'
		loan_type_value = loan + ' value'
		property_type_count = prop + ' count'
		property_type_value = prop + ' value'
		loan_purpose_count = purpose + ' count'
		loan_purpose_value = purpose + ' value'


		if action in self.table_1['action'] and loan_type_count in self.table_1['action'][action] and prop == '1-4 family' or prop == 'manufactured':
			if purpose == 'purchase' and prop != 'multifamly':
				self.table_1['action'][action][loan_type_count] +=1
				self.table_1['action'][action][loan_type_value] += int(inputs['loan_amount'])
			if purpose == 'refinance' or purpose == 'home improvement' and prop != 'multifamily':
				self.table_1['action'][action][loan_purpose_count] += 1
				self.table_1['action'][action][loan_purpose_value] += int(inputs['loan_amount'])
			if prop == 'multifamily':
				self.table_1['action'][action][property_type_count] +=1
				self.table_1['action'][aciton][property_type_value] += int(inputs['loan_amount'])
			if prop != 'multifamly' and occupancy == 'non-occupant':
				self.table_1['action'][action][occupancy_count] += 1
				self.table_1['action'][action][occupancy_value] += int(inputs['loan_amount'])
			if prop == 'manufactured':
				self.table_1['action'][action][property_type_count] +=1
				self.table_1['action'][action][property_type_value] += int(inputs['loan_amount'])
		else:
			print "error, key not in dictionary"

	def print_table_1(self):
		print "\n" *4
		print "originated loans\n", "*" * 10
		for key, value in self.table_1['action']['originated'].iteritems():
			print key, value

		print "\nnot accepted loans\n", "*" * 10
		for key, value in self.table_1['action']['not accepted'].iteritems():
			print key, value

		print "\ndenied applications\n", "*" * 10
		for key, value in self.table_1['action']['denied'].iteritems():
			print key, value

		print "\nwithdrawn applications\n", "*" * 10
		for key, value in self.table_1['action']['withdrawn'].iteritems():
			print key, value

		print "\nincomplete applications\n", "*" * 10
		for key, value in self.table_1['action']['incomplete'].iteritems():
			print key, value

		print "\npurchased loans\n", "*" * 10
		for key, value in self.table_1['action']['purchased'].iteritems():
			print key, value

	#with open('report_1v2.json', 'wb') as outfile:
	#	json.dump(report, outfile)
	def write_report_1_json(self, name):
		import json
		with open(name, 'w') as outfile:
		     json.dump(self.table_1, outfile, sort_\keys = True, indent = 4, ensure_ascii=False)



	#tables 1 and 2 require using: geocode, loanpurpose, occupancy, actiontype, loanvalue
	#census_tract is the 11 digit state/county/tract number for the address of the loan
	#loantype is conventional(1), FHA(2), VA(3), FSA/RHS(4)
	#loanpurpose determines purchase (1), refinance(2), or home improvement(3)
	#occupancy shows owner(1) vs non-owner(2) or not applicable(3) occupancy status
	#actiontype shows the application disposition originated(1), not accepted(2), denied(3), withdrawn(4), incomplete(5), purchased(6)
	#loanvalue is the amount of the loan
	#propertytype determines 1-4 family(1),manufactured housing(2), or multifamily(3)
	def report_1_main(self, location):


		SQL = """SELECT count(censustractnumber) FROM HMDA_LAR_PUBLIC_FINAL_2012 WHERE statecode = %s and countycode = %s and censustractnumber = %s; """
		self.cur.execute(SQL, location)
		#cur.execute("""SELECT count(censustractnumber) FROM HMDA_LAR_PUBLIC_FINAL_2012 WHERE statecode = '31' and countycode = '153' and censustractnumber = '0105.02'; """)

		rows = self.cur.fetchone()
		count = rows[0]

		print count
		SQL = """SELECT
			censustractnumber, loantype, occupancy, loanamount, actiontype, loanpurpose, propertytype,
			statecode, countycode
		 FROM HMDA_LAR_PUBLIC_FINAL_2012
		 where statecode = %s and countycode = %s and censustractnumber = %s; """
		self.cur.execute(SQL, location)
		#cur.execute("""SELECT
		#	censustractnumber, loantype, occupancy, loanamount, actiontype, loanpurpose, propertytype,
		#	statecode, countycode
		 #FROM HMDA_LAR_PUBLIC_FINAL_2012
		 #where statecode = '31' and countycode = '153' and censustractnumber = '0105.02'; """)

		for i in range(0, count):

			row = self.cur.fetchone() # fetches all the rows with census_tracts matching the passed value
			#how many rows were returned?
			#what if no rows are returned? -- all values stay at 0
			#what if more than 1 row is returned -- this code returns all rows in a loop and parses the tuples into the
			#appropriate filters

			#splits the tuples into word variables for easy reading
			self.parse_inputs(row)

			#issues:
			##need to sort geographic identifiers that are NA, invalid or unavailable.
			#build tracts into MSA/MD total
			#State totals may be needed if MSA/MD is not available
			#county totals will be needed

			#the following conditionals section aggregates the counts and values of different loan types and uses the aggregates to fill the dictionary/JSON object
			self.table_1_aggregator(self.inputs)

			#columns 1 and 2 on table 1
			#Government sponsored home purchase
			#home purchase, FHA RSA or VA loan, on 1-4 family, originated

	#output check
	#location = ('31', '153', '0105.02' )
	#main(location)








