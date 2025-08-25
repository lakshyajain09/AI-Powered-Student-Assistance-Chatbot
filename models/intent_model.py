import json
import numpy as np
import pickle
import random
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from sklearn.preprocessing import LabelEncoder

class IntentClassifier:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = None
        self.words = []
        self.classes = []
        self.documents = []
        self.model = None
        self.ignore_letters = ['?', '!', '.', ',']
        
        # Load intents from JSON file
        try:
            with open('data/intents.json', 'r') as file:
                self.intents = json.load(file)
        except FileNotFoundError:
            print("intents.json file not found. Model training will fail.")
    
    def preprocess_data(self):
        # Tokenize and lemmatize all patterns in the intents file
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                word_list = nltk.word_tokenize(pattern)
                self.words.extend(word_list)
                self.documents.append((word_list, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
        
        # Lemmatize and lowercase each word while removing duplicates
        self.words = [self.lemmatizer.lemmatize(word.lower()) for word in self.words 
                     if word not in self.ignore_letters]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))
        
        # Save processed data
        with open('data/words.pkl', 'wb') as file:
            pickle.dump(self.words, file)
        with open('data/classes.pkl', 'wb') as file:
            pickle.dump(self.classes, file)
    
    def create_training_data(self):
        # Create the training data
        training = []
        output_empty = [0] * len(self.classes)
        
        for document in self.documents:
            bag = []
            word_patterns = document[0]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)
            
            output_row = list(output_empty)
            output_row[self.classes.index(document[1])] = 1
            
            training.append([bag, output_row])
        
        # Shuffle and convert to numpy array
        random.shuffle(training)
        training = np.array(training, dtype=object)
        
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])
        
        return np.array(train_x), np.array(train_y)
    
    def build_model(self):
        # Build the neural network model
        model = Sequential()
        model.add(Dense(128, input_shape=(len(self.words),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.classes), activation='softmax'))
        
        # Compile the model
        sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        
        return model
    
    def train(self):
        print("Preprocessing data...")
        self.preprocess_data()
        
        print("Creating training data...")
        train_x, train_y = self.create_training_data()
        
        print("Building model...")
        self.model = self.build_model()
        
        print("Training model...")
        self.model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
        
        # Save the trained model
        self.model.save('models/intent_model.h5')
        print("Model training completed.")
    
    def load_model(self):
        # Load the trained model and data
        try:
            self.model = load_model('models/intent_model.h5')
            with open('data/words.pkl', 'rb') as file:
                self.words = pickle.load(file)
            with open('data/classes.pkl', 'rb') as file:
                self.classes = pickle.load(file)
            with open('data/intents.json', 'r') as file:
                self.intents = json.load(file)
            print("Model and data loaded successfully.")
        except Exception as e:
            print(f"Error loading model or data: {e}")
    
    def _bag_of_words(self, sentence):
        # Tokenize and lemmatize the sentence
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        
        # Create bag of words array
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, word in enumerate(self.words):
                if word == s:
                    bag[i] = 1
        
        return np.array(bag)
    
    def predict(self, sentence):
        if self.model is None:
            self.load_model()
        
        # Get bag of words for the sentence
        bow = self._bag_of_words(sentence)
        
        # Predict intent with the model
        res = self.model.predict(np.array([bow]))[0]
        
        # Get prediction with highest probability
        results = [[i, r] for i, r in enumerate(res)]
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Get the intent tag with highest probability
        return self.classes[results[0][0]]