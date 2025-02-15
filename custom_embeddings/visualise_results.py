import pickle
import numpy as np
import json
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn import preprocessing

normalizer = preprocessing.Normalizer()

with open("saved_embeddings/generated_embeddings.json","r") as f:
    embeddings=dict(json.load(f))

labels = []
tokens = []
for w in embeddings.keys():
    labels.append(w)
    tokens.append(embeddings[w])
tsne_model = TSNE(perplexity=20,n_components=2, random_state=23)
new_values = tsne_model.fit_transform(np.array(tokens))
# new_values =  normalizer.fit_transform(new_values, 'l2')
x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])
    
plt.figure(figsize=(16, 16)) 
for i in range(len(x)):
    plt.scatter(x[i],y[i])
    plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')

plt.savefig("vectors.png")
plt.show()