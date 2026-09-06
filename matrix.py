import copy
import math


class Matrix():
    side_length = 0
    values    = []
    full_vals = []

    def __init__(self, side_length=None, values=None, fullvals=None):
        if fullvals:
            self.full_vals   = copy.deepcopy(fullvals)
            self.side_length = len(self.full_vals)
            self.values      = []
            for val in self.full_vals[0]:
                if val == 0: break
                else:
                    self.values.append(val)
        elif values and side_length:
            self.side_length = side_length
            self.values      = values.copy()
            self.full_vals   = []
            for i in range(0, self.side_length + 1):
                self.full_vals.append([])
                for j in range(0, self.side_length + 1):
                    self.full_vals[i].append(self.get_value_at(i, j))
        else:
            raise Exception("ERROR: Called constructor with invalid arguments!")


    def __mul__(self, other):
        """Operator overload for multiplication.
        """

        if self.side_length != other.side_length:
            raise Exception("ERROR: Multiplying matrices of different sizes!")

        new_vals = []
        while len(self.values) < len(other.values):
            self.values.append(0)
        while len(other.values) < len(self.values):
            other.values.append(0)

        len_self = len(self.values)
        len_other = len(other.values)
        for i in range(0, min(self.side_length, len_self + len_other - 1)):
            lower_bound_self = (((i % len_other) + 1) * math.floor(i / len_other))
            upper_bound_self = min(i, len_self - 1)
            lower_bound_other = min(i, len_other - 1)
            upper_bound_other = (((i % len_self) + 1) * math.floor(i / len_self))

            sum = 0
            for index_self, index_other in zip(range(lower_bound_self, upper_bound_self + 1), reversed(range(upper_bound_other, lower_bound_other + 1))):
                sum += self.values[index_self] * other.values[index_other]
            new_vals.append(sum)

        return Matrix(side_length=self.side_length, values=new_vals)


    def get_value_at(self, i, j):
        index = j - i

        if index < 0 or index >= len(self.values):
            return 0
        else:
            return self.values[index]


    def square_values(self):
        new_vals = []
        for i in range(0, min(self.side_length, (len(self.values) * 2) - 1)):
            lower_bound = ((i % len(self.values)) + 1) * math.floor(i / len(self.values))
            upper_bound = min(i, len(self.values) - 1)
            sum = 0
            for first_index in range(lower_bound, upper_bound + 1):
                second_index = upper_bound - first_index + lower_bound
                sum += self.values[first_index] * self.values[second_index]
            new_vals.append(sum)
        return Matrix(side_length=self.side_length, values=new_vals)


    def multiply_values(self, other):
        if self.side_length != other.side_length:
            raise Exception("ERROR: Multiplying matrices of different sizes!")

        #smaller_set_of_values = min(len(self.values), len(other.values))
        #longer_set_of_values = max(len(self.values), len(other.values))
        new_vals = []
        len_self = len(self.values)
        len_other = len(other.values)
        for i in range(0, min(self.side_length, len_self + len_other - 1)):
            #lower_bound = (((i % longer_set_of_values) + 1) * math.floor(i / longer_set_of_values))
            #upper_bound = min(i, smaller_set_of_values - 1)
            #lower_bound2 = min(i, longer_set_of_values - 1)
            #upper_bound2 = (((i % smaller_set_of_values) + 1) * math.floor(i / smaller_set_of_values))
            upper_bound_other = (((i % len_self) + 1) * math.floor(i / len_self))
            lower_bound_other = min(i, len_other - 1)
            upper_bound_self = min(i, len_self - 1)
            lower_bound_self = (((i % len_other) + 1) * math.floor(i / len_other))
            #print("[" + str(lower_bound) + " " + str(upper_bound) + "]", end="")
            #print("[" + str(lower_bound2) + " " + str(upper_bound2) + "]", end="")
            sum = 0
            for index_self, index_other in zip(range(lower_bound_self, upper_bound_self + 1), reversed(range(upper_bound_other, lower_bound_other + 1))):
                # second_index = upper_bound - first_index + lower_bound
                #second_index = upper_bound
                sum += self.values[index_self] * other.values[index_other]
            new_vals.append(sum)
        return Matrix(side_length=self.side_length, values=new_vals)


    def square_naive(self):
        new_full_vals = []
        for i in range(0, self.side_length):
            new_full_vals.append([])
            for j in range(0, self.side_length):
                result = 0
                for k in range(0, self.side_length):
                    result += self.full_vals[i][k] * self.full_vals[k][j]
                new_full_vals[i].append(result)
        return Matrix(fullvals=new_full_vals)


    def multiply_naive(self, other):
        if self.side_length != other.side_length:
            raise Exception("ERROR: Multiplying matrices of different sizes!")

        new_full_vals = []
        for i in range(0, self.side_length):
            new_full_vals.append([])
            for j in range(0, self.side_length):
                result = 0
                for k in range(0, self.side_length):
                    result += self.full_vals[i][k] * other.full_vals[k][j]
                new_full_vals[i].append(result)

        return Matrix(fullvals=new_full_vals)


    def print(self):
        print()
        for i in range(0, self.side_length):
            for j in range(0, self.side_length):
                value = self.full_vals[i][j]

                if value == 0:
                    print("{0:>7}".format(0), end="")
                else:
                    print("{0:>7.3f}".format(value), end="")
            print()
        print()


    def print_preview(self, max_preview_size=9):
        print()
        for i in range(0, min(self.side_length, max_preview_size)):
            for j in range(0, min(self.side_length, max_preview_size)):
                if i == max_preview_size - 1 or j == max_preview_size - 1:
                    print("{0:>7}".format("..."), end="")
                    continue

                value = self.get_value_at(i, j)

                if value == 0:
                    print("{0:>7}".format(0), end="")
                else:
                    print("{0:>7.3f}".format(value), end="")
            print()
        print()


    def print_values(self):
        print("[", end="")
        for i in range(0, len(self.values)):
            print("{:.3f}".format(self.values[i], 3), end="")
            if i != len(self.values) - 1:
                print(", ", end="")
        print("]", end="")
