from keras.datasets import mnist
from keras.layers import Input, Dense
from keras import regularizers, models, optimizers
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Analytical PCA of the training set
def AnalyticalPCA(y, dimension):
    pca = PCA(n_components=dimension)
    pca.fit(y)
    loadings = pca.components_
    return loadings

# Linear Autoencoder
def LinearAE(y, dimension, learning_rate = 1e-4, regularization = 5e-4, epochs=3):
    input = Input(shape=(y.shape[1],))
    encoded = Dense(dimension, activation='linear',
                    kernel_regularizer=regularizers.l2(regularization))(input)
    decoded = Dense(y.shape[1], activation='linear',
                    kernel_regularizer=regularizers.l2(regularization))(encoded)
    autoencoder = models.Model(input, decoded)
    autoencoder.compile(optimizer=optimizers.adam(lr=learning_rate), loss='mean_squared_error')
    autoencoder.fit(y, y, epochs=epochs, batch_size=4, shuffle=True)
    (w2,b2,w1,b1)=autoencoder.get_weights()
    return (w2,b2,w1,b1)

def PlotResults(p,dimension,name):
    sqrt_dimension = int(np.ceil(np.sqrt(dimension)))
    for i in range(p.shape[0]):
        plt.subplot(sqrt_dimension, sqrt_dimension, i + 1)
        plt.imshow(p[i, :, :],cmap='gray')
        plt.axis('off')
    plt.savefig(name + '.png')

dimension = 16
(y, _), (_, _) = mnist.load_data()
shape_y = y.shape
#print(shape_y )=(60000, 28, 28) #每張圖片都是28*28pixels
y = np.reshape(y,[shape_y[0],shape_y[1]*shape_y[2]]).astype('float32')/255
p_analytical = AnalyticalPCA(y,dimension)
(w2, _, _, _) = LinearAE(y, dimension)
#print(w2.shape)=(784, 16)
(p_linear_ae, _, _) = np.linalg.svd(w2, full_matrices=False)                    # PCA by applying SVD to linear autoencoder weights
p_analytical = np.reshape(p_analytical,[dimension,shape_y[1],shape_y[2]])       # reshape loading vectors before plotting
w2 = np.reshape(w2.T,[dimension,shape_y[1],shape_y[2]])                         # reshape autoencoder weights before plotting
p_linear_ae = np.reshape(p_linear_ae.T, [dimension, shape_y[1], shape_y[2]])    # reshape loading vectors before plotting
PlotResults(p_analytical,dimension,'AnalyticalPCA')
PlotResults(w2,dimension,'W2')
PlotResults(p_linear_ae,dimension,'LinearAE_PCA')
