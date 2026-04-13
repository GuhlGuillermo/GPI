import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, EffectCoverflow } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/effect-coverflow';

const DishRoulette = ({ title, dishes = [], selectedDishId, onSelect }) => {
  if (dishes.length === 0) return null;

  return (
    <div className="py-8 border-b border-slate-100">
      <h3 className="text-xl font-bold text-brand-dark mb-6 flex items-center gap-3 px-8">
         <span className="bg-brand-dark text-white rounded-full w-8 h-8 flex items-center justify-center text-sm">✓</span> 
         {title}
      </h3>
      
      <div className="w-full relative px-4">
        <Swiper
          effect={'coverflow'}
          grabCursor={true}
          centeredSlides={true}
          slidesPerView={'auto'}
          coverflowEffect={{
            rotate: 50,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: true,
          }}
          pagination={{ clickable: true }}
          navigation={true}
          modules={[EffectCoverflow, Pagination, Navigation]}
          className="w-full max-w-3xl mx-auto py-10"
        >
          {dishes.map((dish) => (
            <SwiperSlide key={dish.id_plato} className="max-w-[280px] sm:max-w-[320px]">
              <div 
                className={`bg-white rounded-2xl overflow-hidden shadow-lg border-2 transition-all cursor-pointer transform hover:scale-105 ${selectedDishId === dish.id_plato ? 'border-brand-primary ring-4 ring-brand-primary/20' : 'border-transparent'}`}
                onClick={() => onSelect(dish)}
              >
                <div className="h-48 w-full bg-slate-100 relative">
                  {/* Imagen de fallback manejada por backend, pero por si acaso reventara */}
                  <img src={dish.url_imagen || '/default-dish.png'} alt={dish.nombre_plato} className="w-full h-full object-cover" onError={(e) => { e.target.onerror = null; e.target.src='/default-dish.png'; }} />
                  {selectedDishId === dish.id_plato && (
                     <div className="absolute top-3 right-3 bg-brand-primary text-white p-2 rounded-full shadow-md z-10 w-8 h-8 flex items-center justify-center">✓</div>
                  )}
                </div>
                <div className="p-5">
                  <h4 className="font-bold text-lg text-slate-800 mb-2 truncate">{dish.nombre_plato}</h4>
                  <p className="text-sm text-slate-500 line-clamp-2 h-10">{dish.descripcion}</p>
                </div>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </div>
  );
};

export default DishRoulette;
