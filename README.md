# HighFashion Design Studio

## Environment

### Back-end

- Python 2.7
- Django 1.9
- Django REST framework 3.3
- MySQL 5.5

### Front-end

- Base Template
	- Introduce : [Spectral | HTML5 UP](http://html5up.net/spectral)
	- Design Studio : [Gentelella](https://github.com/puikinsh/gentelella)
- Single-page Application

## Demo

[HighFashion](http://highfashion.pro/)

## Component

### Gallery

#### Top 10.

사용자들을 통해서 만든 Fashion Image 들이 전시.
좋아요를 많이 받은 순서대로 10개의 Image만.

####  Collection

각 단어들을 통해서 만든 패션이미지들을 조회.

### Design Step

1. **Scatch** 
	- [DCGAN(Deep Convolutional Generative Adversarial Networks)](https://github.com/Soma2-HighFashion/Word2Image/tree/master/dcgan)
	- Word2Vec - Pre-trained model : [GoogleNews-vectors-negative300](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit)
	- => Word2Image
2. **Filter**
	- [Caman.js](http://camanjs.com/)
3. **Design Detail**
	- Image Analysis(Gender, Category) - Simple CNN, ResNet
4. **Look Similar Fashion**
	- [LSHForest](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LSHForest.html)(k=12)
