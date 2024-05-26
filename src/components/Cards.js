import React from 'react';
import './Cards.css';
import CardItem from './CardItem';

import img1 from '../images/cards-section/cards-img-1.webp'; 
import img2 from '../images/cards-section/cards-img-2.webp';
import img3 from '../images/cards-section/cards-img-3.webp';
import img4 from '../images/cards-section/cards-img-4.webp';
import img5 from '../images/cards-section/cards-img-5.webp';
import img6 from '../images/cards-section/cards-img-6.webp';


function Cards() {
  return (
    <div className='cards'>
      <h1>Check out the Most Recent Notes Left!</h1>
      <div className='cards__container'>
        <div className='cards__wrapper'>
          <ul className='cards__items'>
            <CardItem
              src={img6}
              text='Software Engineering'
              label='CSC 423'
              path='/services'
            />
            <CardItem
              src={img2}
              text='Theory of Computation'
              label='CSC 311'
              path='/services'
            />
          </ul>
          <ul className='cards__items'>
            <CardItem
              src={img4}
              text='Data Structures'
              label='CSC 313'
              path='/services'
            />
            <CardItem
              src={img3}
              text='Calculus III'
              label='MAT 213'
              path='/products'
            />
            <CardItem
              src={img5}
              text='Analysis of Algorithms'
              label='CSC 325'
              path='/products'
            />
            <CardItem
              src={img1}
              text='Introduction to Artificial Intelligence'
              label='CSC 432'
              path='/sign-up'
            />
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Cards;
