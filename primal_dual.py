def construct_dual(objective_value_function,cost_vector,constraints_vector,coefficients_matrix):
	if objective_value_function=="maximization":
		dual_objective_function = "minimization"
	else:
		dual_objective_function = "maximization"

	dual_coefficients_matrix = []
	for j in range(len(coefficients_matrix[0])):
		temp = []
		for i in range(len(coefficients_matrix)):
			temp.append(coefficients_matrix[i][j])
		dual_coefficients_matrix.append(temp)


	return [dual_objective_function,cost_vector,constraints_vector,dual_coefficients_matrix]



def get_initial_lambda(dual_constraints_vector,dual_coefficients_matrix):
	minimum_index = dual_constraints_vector.index(min(dual_constraints_vector))
	minimum_value = dual_constraints_vector[minimum_index]
	result = None
	for i in range(minimum_value):
		temp = dual_coefficients_matrix[minimum_index][0]*i
		for j in range(minimum_value+1):
			temp1 = dual_coefficients_matrix[minimum_index][1]*j
			if temp+temp1<=minimum_value:
				result = (i,j)
				#break
	return result



def construct_arp(primal_cost_vector,primal_number_of_constraints,primal_constraints_vector,primal_objective_value_function,primal_coefficients_matrix,lambda_value):
	arp_cost_vector = [0]*len(primal_cost_vector)
	arp_cost_vector.extend([1]*primal_number_of_constraints)
	arp_coefficient_matrix = []
	identity_matrix = []

	for i in range(primal_number_of_constraints):
		identity_matrix.append([0]*primal_number_of_constraints)
	
	for i in range(len(primal_coefficients_matrix)):
		temp = []
		for j in range(len(primal_coefficients_matrix[0])):
			temp.append(primal_coefficients_matrix[i][j])
		identity_matrix[i][i] = 1
		temp.extend(identity_matrix[i])
		temp.append(primal_constraints_vector[i])
		arp_coefficient_matrix.append(temp)

	temp = []	
	for j in range(len(primal_coefficients_matrix[0])):
		s=0
		for i in range(len(primal_coefficients_matrix)):
			s-=primal_coefficients_matrix[i][j]
		temp.append(s)
	temp.extend([0]*(len(arp_coefficient_matrix[-1])-len(temp)))
	arp_coefficient_matrix.append(temp)
	temp = []
	for j in range(len(primal_coefficients_matrix[0])):
		s=0
		for i in range(len(primal_coefficients_matrix)):
			s+=primal_coefficients_matrix[i][j]*lambda_value[i]
		if primal_objective_value_function=="minimization":
			temp.append(primal_cost_vector[j]-s)
		else:
			temp.append(-primal_cost_vector[j]-s)
	temp.extend([0]*(len(arp_coefficient_matrix[-1])-len(temp)))
	arp_coefficient_matrix.append(temp)
	arp_constraints_vector = primal_constraints_vector
	for i in range(len(arp_coefficient_matrix)-len(arp_constraints_vector)):
		arp_constraints_vector.append(0)
	return [primal_objective_value_function,arp_constraints_vector,arp_cost_vector,arp_coefficient_matrix]



def change_arp_table(arp_coefficient_matrix,primal_constraints_vector,primal_coefficients_matrix):
	ratios = []
	for i in range(len(primal_coefficients_matrix[-1])):
		if arp_coefficient_matrix[-2][i]!=0: 
			ratios.append(arp_coefficient_matrix[-1][i]/abs(arp_coefficient_matrix[-2][i]))
	minimum_ratio = min(ratios)

	for i in range(len(primal_coefficients_matrix[-1])):
		arp_coefficient_matrix[-1][i] = arp_coefficient_matrix[-1][i]+arp_coefficient_matrix[-2][i]*minimum_ratio

	return arp_coefficient_matrix




def arp_simplex(arp_cost_vector,arp_constraints_vector,arp_coefficient_matrix,primal_constraints_vector,primal_coefficients_matrix,primal_cost_vector):
	basis = []
	slack_variables = []
	for i in range(len(arp_cost_vector)):
		if arp_cost_vector[i]==1:
			basis.append(i)
			slack_variables.append(i)

	while True:
		q = None
		for i in range(len(primal_cost_vector)):
			if arp_coefficient_matrix[-1][i]==0 and i not in basis:
				q = i
				break
		if q==None:
			break
		s = 1000000
		p = None
		for i in range(len(primal_coefficients_matrix)):
			if arp_coefficient_matrix[i][q]>0:
				k = arp_coefficient_matrix[i][-1]/arp_coefficient_matrix[i][q]
				if k>0 and s>k:
					s=k
					p=i
		if p==None:
			print("infeasible")
			return
		pivot = arp_coefficient_matrix[p][q]
		#print(pivot)
		for i in range(len(arp_coefficient_matrix[-1])):
			arp_coefficient_matrix[p][i] = arp_coefficient_matrix[p][i]/pivot


		for i in range(len(arp_coefficient_matrix)):
			temp = []
			for j in range(len(arp_coefficient_matrix[-1])):
				if i!=p:
					temp.append(arp_coefficient_matrix[i][j] - ((arp_coefficient_matrix[i][q]/arp_coefficient_matrix[p][q])*arp_coefficient_matrix[p][j]))
			if i!=p:
		 		arp_coefficient_matrix[i] = temp
		basis[p]=q
		#print(basis)
		if any([i for i in basis if i in slack_variables]):
			arp_coefficient_matrix = change_arp_table(arp_coefficient_matrix,primal_constraints_vector,primal_coefficients_matrix)
		else:
			break
	
	if any([i for i in basis if i in slack_variables]):
		print("unboundedness")
		return

			
	result = [0]*len(primal_coefficients_matrix[-1])
	for i in range(len(primal_coefficients_matrix)):
		result[basis[i]] = arp_coefficient_matrix[i][-1]

	total = 0
	for i in range(len(primal_cost_vector)):
		total+=primal_cost_vector[i]*result[i]
	print(total)


primal_cost_vector = list(map(int,input("Enter cost coefficients: ").split()))
#initial_cost_vector_length = len(cost_vector)
primal_number_of_constraints = int(input("Enter number of constraints: "))
#total_constraints_length = len(cost_vector)+number_of_constraints
primal_coefficients_matrix = list()
print("Enter coefficients: ")

for i in range(primal_number_of_constraints):
	l = list(map(int,input().split()))
	primal_coefficients_matrix.append(l)

primal_constraints_vector = list(map(int,input("Enter constraints: ").split()))

primal_objective_value_function = input("Enter objective value function: ")

dual = construct_dual(primal_objective_value_function,primal_cost_vector,primal_constraints_vector,primal_coefficients_matrix)
dual_objective_function = dual[0]
dual_cost_vector = dual[2]
dual_constraints_vector = dual[1]
dual_coefficients_matrix = dual[3]


lambda_value = get_initial_lambda(dual_constraints_vector,dual_coefficients_matrix)
#lambda_value = (0,0)
arp = construct_arp(primal_cost_vector,primal_number_of_constraints,primal_constraints_vector,primal_objective_value_function,primal_coefficients_matrix,lambda_value)
arp_objective_value_function = arp[0]
arp_cost_vector = arp[2]
arp_constraints_vector = arp[1]
arp_coefficient_matrix = arp[3]

arp_simplex(arp_cost_vector,arp_constraints_vector,arp_coefficient_matrix,primal_constraints_vector,primal_coefficients_matrix,primal_cost_vector)