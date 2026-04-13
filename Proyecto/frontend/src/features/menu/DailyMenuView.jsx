import React, { useState, useEffect } from 'react';
import { apiClient } from '../../core/api';
import DishRoulette from './components/DishRoulette';

const DailyMenuView = () => {
  const [dishes, setDishes] = useState({
    starters: [],
    mains: [],
    desserts: []
  });
  const [loading, setLoading] = useState(true);

  const [selectedStarter, setSelectedStarter] = useState(null);
  const [selectedMain, setSelectedMain] = useState(null);
  const [selectedDessert, setSelectedDessert] = useState(null);
  
  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const res = await apiClient.get('/dishes');
        const allDishes = res.data;
        
        setDishes({
          starters: allDishes.filter(d => d.categoria === 'ENTRANTE'),
          mains: allDishes.filter(d => d.categoria === 'PRINCIPAL'),
          desserts: allDishes.filter(d => d.categoria === 'POSTRE')
        });
      } catch (err) {
        console.error("Error cargando platos", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMenu();
  }, []);

  const isMenuSelected = selectedStarter && selectedMain && selectedDessert;

  if(loading) return <div className="text-center py-20 text-slate-500 font-bold text-xl animate-pulse">Precalentando cocinas...</div>;

  return (
    <div className="max-w-6xl mx-auto animate-fade-in pb-10">
      <div className="text-center mb-12">
        <h2 className="text-5xl font-display font-black text-slate-800">Menú del Día</h2>
        <div className="mt-4 flex items-center justify-center gap-4">
            <div className="h-px bg-slate-200 w-16"></div>
            <span className="text-3xl font-bold bg-amber-100 text-amber-700 px-6 py-2 rounded-2xl border border-amber-200">15.00€</span>
            <div className="h-px bg-slate-200 w-16"></div>
        </div>
        <p className="text-slate-500 mt-6 max-w-lg mx-auto">Selecciona una opción de cada sección para completar tu menú. Incluye bebida o agua sin recargo.</p>
      </div>

      <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100 mb-8">
        <DishRoulette 
          title="1. Elige tu Entrante" 
          dishes={dishes.starters} 
          selectedDishId={selectedStarter?.id_plato} 
          onSelect={setSelectedStarter} 
        />
        <DishRoulette 
          title="2. Plato Principal" 
          dishes={dishes.mains} 
          selectedDishId={selectedMain?.id_plato} 
          onSelect={setSelectedMain} 
        />
        <DishRoulette 
          title="3. Un toque dulce" 
          dishes={dishes.desserts} 
          selectedDishId={selectedDessert?.id_plato} 
          onSelect={setSelectedDessert} 
        />
      </div>

      {/* Checkout inferior dedicado al Menú - DESHABILITADO TEMPORALMENTE */}
      {/*
      <div className="flex flex-col md:flex-row items-center justify-between p-6 bg-slate-900 rounded-2xl shadow-xl sticky bottom-4 z-50">
         <div className="mb-4 md:mb-0">
             <span className="block text-slate-400 text-sm mb-1">
               {selectedStarter?.nombre_plato || '---'} | {selectedMain?.nombre_plato || '---'} | {selectedDessert?.nombre_plato || '---'}
             </span>
             <span className="text-white font-bold text-2xl font-display">15.00€</span>
         </div>
         <button 
           className="w-full md:w-auto bg-brand-accent hover:bg-yellow-500 disabled:opacity-50 disabled:bg-slate-700 text-slate-900 disabled:text-slate-400 px-10 py-4 rounded-xl font-bold text-lg transition-all cursor-pointer transform hover:scale-105 active:scale-95"
           disabled={!isMenuSelected}
         >
           {isMenuSelected ? 'Añadir Menú al Pedido' : 'Selecciona las 3 opciones'}
         </button>
      </div>
      */}
    </div>
  );
};

export default DailyMenuView;
