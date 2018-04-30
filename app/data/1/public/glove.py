from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

glove2word2vec(glove_input_file="glove.6B.300d.txt", word2vec_output_file="gensim_glove_vectors.txt")

analogy_pos =  [
               ['queen','male'],
               ['smile','pain'],
               ['afghanistan','madrid'],
               ['best','bad'],
               ['rupee','america'],
               ['rupee','france'],
               ['quench','hunger'],
               ['ebb','moon'],
               ['man','queen'],
               ['king','woman'],
               ['usual','occasionally'],
               ['down','left'],
               ['cat','bark'],
               ['cat','puppy'],
               ['walk','made'],
               ['unable','can'],
               ['dirty','big'],
               ['men','goose'],
               ['snake','mammal'],
               ['baker','cook'],
               ['went','read'],
              ]

analogy_neg = [
               ['king'],
               ['pleasure'],
               ['spain'],
               ['good'],
               ['india'],
               ['india'],
               ['thirst'],
               ['tide'],
               ['woman'],
               ['man'],
               ['occasional'],
               ['right'],
               ['dog'],
               ['dog'],
               ['make'],
               ['able'],
               ['clean'],
               ['man'],
               ['bat'],
               ['bake'],
               ['go'],
           ]

expected = [
           ['female'],
           ['grimace'],
           ['kabul'],
           ['worst'],
           ['dollar'],
           ['euro'],
           ['sate'],
           ['wane'],
           ['king'],
           ['queen'],
           ['usually'],
           ['up'],
           ['purr'],
           ['kitten'],
           ['walked'],
           ['cannot'],
           ['small'],
           ['geese'],
           ['reptile'],
           ['chef'],
           ['read'],
          ]

# load the Stanford GloVe model
filename = 'gensim_glove_vectors.txt'

print("Using the Glove Vectors")

model = KeyedVectors.load_word2vec_format(filename, binary=False)
# calculate: (king - man) + woman = ?

for i in range(len(analogy_pos)):
   result = model.most_similar(positive=analogy_pos[i], negative=analogy_neg[i], topn=3)
   print('Given answer: ',result)
   print('Expected answer: ',expected[i])
   print('\n')