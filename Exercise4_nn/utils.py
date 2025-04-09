import inspect

class Grader():
    grader = None
    token = ""

    def __init__(self):
        self.grader =    { 
            "data": {
                'assignment_nr':"4",
                'assignment_code':"a14cc1ce",
                'createDatasetSplits': {'name':'Dataset preparation', 'score':0,'maxscore':10, 'value': None, 'func_str':'', 'feedback':''},
                'extract_features': {'name':'Plain image feature', 'score':0, 'maxscore':10,'value': None, 'func_str':'', 'feedback':''},
                'cnnTraining': {'name':'CNN Training (Cats vs. Dogs)', 'score':0,'maxscore':35, 'value': None, 'func_str':'', 'feedback':''},
                'cnnTest': {'name':'CNN Test (Cats vs. Dogs)', 'score':0,'maxscore':20, 'value': None, 'func_str':'', 'feedback':''},
                'compute_confusion_matrix_plot': {'name':'Confusion Matrix (Cats vs. Dogs)', 'score':0,'maxscore':10, 'value': None, 'func_str':'', 'feedback':''},
                'pred_all_test': {'name':'CNN Train (All animals)', 'score':0,'maxscore':15, 'value': None, 'func_str':'', 'feedback':''},
                'pred_all_test_optimized': {'name':'Optimization (optional), pred accuracy:', 'score':0,'maxscore':0, 'value': None, 'func_str':'', 'feedback':''},
            }
        }


    def setFunc(self, id, func):
        code_str = inspect.getsource(func)
        self.grader["data"][id]["func_str"]=code_str
    
    def setValue(self, id, value):
        self.grader["data"][id]["value"]=value

    def setToken(self, token):
        self.token = token


   # Evaluate the different parts of exercise
    def grade(self):

        # get results from remote
        result = self.submit()
 
        # Print the grading table
        if not result:
            return

        reachedScore = 0
        maxScore = 0
        for id, part in result.items():
            if "assignment_" in id:
                continue
            score = '%d / %3d' % (part["score"], part["maxscore"])
            print('%43s | %9s | %-s' % (part["name"], score, part["feedback"]))
            reachedScore += part["score"]
            maxScore += part["maxscore"]
        total_score = '%d / %d' % (reachedScore,maxScore)
        print('                                  --------------------------------')
        print('%43s | %9s | %-s\n' % ("", total_score, ""))


    def submit(self):
            import requests
            import json
            
            url = "http://evalml.da.private.hm.edu/result_receiver/"
            
            head = {'Authorization': 'token {}'.format(self.token)}
            
            response = requests.post(url, json=self.grader, headers=head)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                return False