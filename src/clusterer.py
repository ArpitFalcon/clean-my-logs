import re
from .pattern_generator import PatternGenerator
from .scorer import Scorer

class Clusterer():
    def __init__(self, k1=1, k2=0.5, delimeters='\\s', max_dist=0.30):
        self.k1 = k1
        self.k2 = k2
        self.delimeters = delimeters
        self.max_dist = max_dist
        self.pattern_generator = PatternGenerator()
        self.scorer = Scorer(k1, k2)

        # List of all the clusters we get (for output)
        # [representative (generalised format), count (of that format)]
        self.clusters = []
    
    def cluster(self, line):
        """Process each line one by one with all the existing clusters."""
        # Convert log data to keywords -> make a class to do comprehensive cleaning
        line = re.sub(r'[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*' , '<ip>', line)
        line = re.sub(r'^(\d{2}):(\d{2}):(\d{2}) ?([AaPp][Mm])$', '<time>', line) # converting only time as there are a lot of formats of date

        tokens = re.split(self.delimeters, line.strip())
        found = False # Pattern found for this line

        for i in range(len(self.clusters)):
            [rep, count] = self.clusters[i]
            
            score = self.scorer.distance(rep, tokens)
            if score <= self.max_dist:
                self.clusters[i][1] += 1 # increment count

                pattern = self.pattern_generator.create_pattern(tokens, rep)
                self.clusters[i][0] = pattern # update the generalised format

                found = True
                break
        
        if not found:
            self.clusters.append([tokens, 1])

    def result(self):
        """Return the clusters made till now"""
        return self.clusters