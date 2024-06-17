class CandidateElimination:
    def __init__(self, num_attributes):
        self.num_attributes = num_attributes
        self.S = [['0'] * num_attributes]  # Most specific hypothesis
        self.G = [['?'] * num_attributes]  # Most general hypothesis

    def eliminate(self, X, Y):
        for i, x in enumerate(X):
            if Y[i] == '1':  # Positive example
                self.generalize_specific(x)
                self.specialize_general(x)
            else:  # Negative example
                self.specialize_specific(x)
                self.generalize_general(x)

    def generalize_specific(self, x):
        for i in range(len(self.S)):
            for j in range(self.num_attributes):
                if self.S[i][j] == '0':  # Initially most specific
                    self.S[i][j] = x[j]
                elif self.S[i][j] != x[j]:
                    self.S[i][j] = '?'

    def specialize_general(self, x):
        to_remove = []
        for g in self.G:
            if not self.match(x, g):
                to_remove.append(g)
                for j in range(self.num_attributes):
                    if g[j] == '?':
                        new_hypothesis = g[:]
                        new_hypothesis[j] = x[j]
                        if self.consistent_with_any_positive(new_hypothesis):
                            self.G.append(new_hypothesis)
        for g in to_remove:
            self.G.remove(g)
        self.remove_more_general()

    def specialize_specific(self, x):
        to_remove = []
        for s in self.S:
            if self.match(x, s):
                to_remove.append(s)
                for j in range(self.num_attributes):
                    if s[j] != '?' and s[j] != x[j]:
                        new_hypothesis = s[:]
                        new_hypothesis[j] = '?'
                        if self.consistent_with_any_negative(new_hypothesis):
                            self.S.append(new_hypothesis)
        for s in to_remove:
            self.S.remove(s)
        self.remove_more_specific()

    def generalize_general(self, x):
        to_remove = []
        for g in self.G:
            for j in range(self.num_attributes):
                if g[j] == '?':
                    new_hypothesis = g[:]
                    new_hypothesis[j] = x[j]
                    if self.consistent_with_any_negative(new_hypothesis):
                        to_remove.append(g)
                        self.G.append(new_hypothesis)
        for g in to_remove:
            self.G.remove(g)
        self.remove_more_general()

    def consistent_with_any_positive(self, hypothesis):
        for s in self.S:
            if self.match(s, hypothesis):
                return True
        return False

    def consistent_with_any_negative(self, hypothesis):
        for g in self.G:
            if not self.match(hypothesis, g):
                return True
        return False

    def match(self, example, hypothesis):
        for i in range(self.num_attributes):
            if hypothesis[i] != '?' and hypothesis[i] != example[i]:
                return False
        return True

    def remove_more_general(self):
        to_remove = []
        for g in self.G:
            for other in self.G:
                if g != other and self.more_general(g, other):
                    to_remove.append(g)
                    break
        for g in to_remove:
            self.G.remove(g)

    def remove_more_specific(self):
        to_remove = []
        for s in self.S:
            for other in self.S:
                if s != other and self.more_specific(s, other):
                    to_remove.append(s)
                    break
        for s in to_remove:
            self.S.remove(s)

    def more_general(self, h1, h2):
        more_general_or_equal = False
        for i in range(self.num_attributes):
            if h1[i] == '?' or (h1[i] == h2[i]):
                more_general_or_equal = True
            elif h2[i] != '?':
                return False
        return more_general_or_equal

    def more_specific(self, h1, h2):
        more_specific_or_equal = False
        for i in range(self.num_attributes):
            if h2[i] == '?' or (h1[i] == h2[i]):
                more_specific_or_equal = True
            elif h1[i] != '?':
                return False
        return more_specific_or_equal

    def get_hypotheses(self):
        return self.S, self.G

# Example usage:

# Define training data (X) and corresponding labels (Y)
X = [
    ['Sunny', 'Warm', 'Normal', 'Strong'],
    ['Sunny', 'Warm', 'High', 'Strong'],
    ['Rainy', 'Cold', 'High', 'Strong'],
    ['Sunny', 'Warm', 'High', 'Strong']
]
Y = ['1', '1', '0', '1']  # 1 for positive, 0 for negative

num_attributes = len(X[0])
ce = CandidateElimination(num_attributes)

# Apply the algorithm
ce.eliminate(X, Y)

# Get the final hypotheses
S, G = ce.get_hypotheses()

print("Final Specific Hypothesis (S):", S)
print("Final General Hypothesis (G):", G)
