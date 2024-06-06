import React from 'react';
import { useTranslation } from 'react-i18next';


import './BikeList.css'
import BikeListItem from '../components/BikeListItem'

const BikeList = () => {

    const { t } = useTranslation();

    // TODO: implement fetching
    let bikes = [
        {
            id: 1,
            name: 'Lastenrad 1',
            image: require('./bike1.jpg')
        },
        {
            id: 2,
            name: 'Lastenrad 2',
            image: require('./bike2.jpg')
        },
        {
            id: 3,
            name: 'Lastenrad 3',
            image: require('./bike3.jpg')
        },
        {
            id: 4,
            name: 'Lastenrad 4',
            image: require('./bike4.jpg')
        }
    ]

    return (
        <>
            <h1>{t('bikes')}</h1>


            <div className='button-container'>
                
                {/* TODO add sorting buttons */}

                <button type='button' className='new-bike-button'>{t('add_new_bike')}</button>
            </div>

            <ul className='list'>
                {bikes.map((bike) => (
                    <BikeListItem bike={bike} key={bike.id}/>
                ))}
            </ul>

            {/* <img className='img' alt='name' src={require('../assets/images/bike1.jpg')}></img> */}
            
        </>
    );
};
  
export default BikeList;