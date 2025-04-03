import evaluate
import numpy as np

# import accuracy evaluation metric
accuracy = evaluate.load("accuracy")


# define an evaluation function to pass into trainer later
def compute_metrics(p):
    logits, labels = p
    predictions = np.argmax(logits, axis=1)
    accuracy_result = accuracy.compute(predictions=predictions, references=labels)

    return {"accuracy": accuracy_result["accuracy"]}
