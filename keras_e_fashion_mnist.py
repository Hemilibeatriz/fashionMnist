# -*- coding: utf-8 -*-
"""Keras e Fashion-MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nMS-2q8GBJBQvsBVH_VHWS9xhpYIRSEZ

Bibliotecas
"""

import tensorflow
from tensorflow import keras
from keras.models import model_from_json
import matplotlib.pyplot as plt
import numpy as np

"""importando o dataset e separando entre treinamento e teste"""

dataset = keras.datasets.fashion_mnist
((imagens_treino, classes_treino), (imagens_teste, classes_teste)) = dataset.load_data()

"""informações """

print("imagens de Treino:" ,len(imagens_treino))
print("imagens de Treino:" ,imagens_treino.shape)
print("imagens de Teste:" ,imagens_teste.shape)
print("classes de Treino:" ,classes_treino.shape)

print("min: ", classes_treino.min())
print("max: ", classes_treino.max())

nomes_de_classificacoes = ['Camiseta', 'Calça', 'Pullover', 'Vestido', 'Casaco', 'Sandália', 'Camisa', 'Tenis', 'Bolsa', 'Bota']

total_de_classificacoes=10

fig, axes = plt.subplots(figsize=(10,5))
fig.tight_layout()

for imagem in range(10):
   plt.subplot(2, 5, imagem+1)
   plt.imshow(imagens_treino[imagem])
   plt.title(nomes_de_classificacoes[classes_treino[imagem]])

"""uma única imagem

"""

plt.imshow(imagens_treino[0])
plt.colorbar()

"""modelo"""

imagens_treino = imagens_treino/255

modelo = keras.Sequential([keras.layers.Flatten(input_shape=(28,28)),
                           keras.layers.Dropout(0.2),
                           keras.layers.Dense(256, activation=tensorflow.nn.relu),
                           keras.layers.Dense(128, activation=tensorflow.nn.relu),
                           keras.layers.Dense(64, activation=tensorflow.nn.relu),
                           keras.layers.Dense(10, activation=tensorflow.nn.softmax)
                           ])

modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')

"""treinamento"""

hist=modelo.fit(imagens_treino, classes_treino, epochs=10, validation_split=0.2)

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Acurácia por épocas')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')
plt.legend(['Treino', 'Validação'])

plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Loss por épocas')
plt.xlabel('Épocas')
plt.ylabel('Loss')
plt.legend(['Treino', 'Validação'])

model_json = modelo.to_json()
with open("model.json", "w") as json_file:
   json_file.write(model_json)

modelo.save_weights("model.h5")
print("Modelo Salvo")

json_file = open("model.json", "r")
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")
print("Modelo Carregado")

loaded_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')

"""testes"""

perda_teste, acuracia_teste = loaded_model.evaluate(imagens_teste, classes_teste)
print("Perda do teste: ", perda_teste)
print("Acurácia do teste: ", acuracia_teste)
testes=loaded_model.predict(imagens_teste/255)

x=0
arr=[]
for i in testes:
   #print(i)
   print(nomes_de_classificacoes[np.argmax(i)], np.max(i), nomes_de_classificacoes[classes_teste[x]])
   
   if (nomes_de_classificacoes[np.argmax(i)] != nomes_de_classificacoes[classes_teste[x]]):
      arr.append([nomes_de_classificacoes[np.argmax(i)], nomes_de_classificacoes[classes_teste[x]], imagens_teste[x]])
   x=x+1

x=1
for i in arr:
   plt.subplots(1)
   plt.imshow(i[2])
   plt.title("Classe errada= " + i[0] + " Classe correta= " +i[1])
   x=x+1
   if x==10:
      break

modelo.summary()