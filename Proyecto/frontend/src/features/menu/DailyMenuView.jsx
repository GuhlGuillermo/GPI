import React, { useState } from 'react';

const DailyMenuView = ({ onAdd }) => {
  const [selectedStarter, setSelectedStarter] = useState('');
  const [selectedMain, setSelectedMain] = useState('');
  const [selectedDessert, setSelectedDessert] = useState('');
  
  // Condición simulada: si es Sábado, o pasadas las 16h, no debería ni salir. 
  // En React llamaríamos a backend para ver si existe un menú. Simulamos que sí existe uno.
  const isMenuSelected = selectedStarter && selectedMain && selectedDessert;
  const handleAddMenu = () => {
    // Creamos el objeto que representa el menú completo para el carrito
    const menuSelection = {
      dish_id: 'MENU-DIARIO', // ID genérico para identificar que es un menú
      name: `Menú: ${selectedStarter}, ${selectedMain} y ${selectedDessert}`,
      snapshot_price: 15.00, // Precio fijo por REQ 2 
      quantity: 1
    };

    // Llamamos a la función onAdd que viene de App.jsx
    onAdd(menuSelection);

    // Feedback para el usuario y limpiar selección
    alert("¡Menú añadido con éxito!");
    setSelectedStarter('');
    setSelectedMain('');
    setSelectedDessert('');
  };

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      
      <div className="text-center mb-12">
        <h2 className="text-5xl font-display font-black text-slate-800">Menú del Día</h2>
        <div className="mt-4 flex items-center justify-center gap-4">
            <div className="h-px bg-slate-200 w-16"></div>
            <span className="text-3xl font-bold bg-amber-100 text-amber-700 px-6 py-2 rounded-2xl border border-amber-200">15.00€</span>
            <div className="h-px bg-slate-200 w-16"></div>
        </div>
        <p className="text-slate-500 mt-6 max-w-lg mx-auto">Selecciona una opción de cada sección para completar tu menú. Incluye bebida o agua sin recargo.</p>
      </div>

      <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
        
        {/* SECCIÓN 1 */}
        <div className="p-8 border-b border-slate-100 bg-slate-50">
          <h3 className="text-xl font-bold text-brand-dark mb-6 flex items-center gap-3">
             <span className="bg-brand-dark text-white rounded-full w-8 h-8 flex items-center justify-center text-sm">1</span> 
             Elige tu Entrante
          </h3>
          <div className="space-y-3">
            {['Sopa de Lentejas', 'Samosa Vegetal', 'Papadum Especiado'].map(opt => (
              <label key={opt} className={`flex items-center p-4 rounded-xl cursor-pointer transition-colors border ${selectedStarter === opt ? 'border-brand-primary bg-rose-50' : 'border-slate-200 bg-white hover:bg-slate-100'}`}>
                <input type="radio" name="starter" value={opt} onChange={() => setSelectedStarter(opt)} className="hidden" />
                <div className={`w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center ${selectedStarter === opt ? 'border-brand-primary' : 'border-slate-300'}`}>
                  {selectedStarter === opt && <div className="w-2.5 h-2.5 bg-brand-primary rounded-full"></div>}
                </div>
                <span className="font-medium text-slate-700">{opt}</span>
              </label>
            ))}
          </div>
        </div>

        {/* SECCIÓN 2 */}
        <div className="p-8 border-b border-slate-100">
          <h3 className="text-xl font-bold text-brand-dark mb-6 flex items-center gap-3">
             <span className="bg-brand-dark text-white rounded-full w-8 h-8 flex items-center justify-center text-sm">2</span> 
             Plato Principal
          </h3>
          <div className="space-y-3">
            {['Pollo al Curry Suave', 'Cordero Biryani (+1€)', 'Garbanzos Chana Masala (Vegano)'].map(opt => (
              <label key={opt} className={`flex items-center p-4 rounded-xl cursor-pointer transition-colors border ${selectedMain === opt ? 'border-brand-primary bg-rose-50' : 'border-slate-200 bg-white hover:bg-slate-100'}`}>
                <input type="radio" name="main" value={opt} onChange={() => setSelectedMain(opt)} className="hidden" />
                <div className={`w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center ${selectedMain === opt ? 'border-brand-primary' : 'border-slate-300'}`}>
                  {selectedMain === opt && <div className="w-2.5 h-2.5 bg-brand-primary rounded-full"></div>}
                </div>
                <span className="font-medium text-slate-700">{opt}</span>
              </label>
            ))}
          </div>
        </div>

        {/* SECCIÓN 3 */}
        <div className="p-8 bg-slate-50">
          <h3 className="text-xl font-bold text-brand-dark mb-6 flex items-center gap-3">
             <span className="bg-brand-dark text-white rounded-full w-8 h-8 flex items-center justify-center text-sm">3</span> 
             Un toque Dulce (Postre)
          </h3>
          <div className="space-y-3">
            {['Gulab Jamun', 'Yogur Helado', 'No deseo postre (Café)'].map(opt => (
              <label key={opt} className={`flex items-center p-4 rounded-xl cursor-pointer transition-colors border ${selectedDessert === opt ? 'border-brand-primary bg-rose-50' : 'border-slate-200 bg-white hover:bg-slate-100'}`}>
                <input type="radio" name="dessert" value={opt} onChange={() => setSelectedDessert(opt)} className="hidden" />
                <div className={`w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center ${selectedDessert === opt ? 'border-brand-primary' : 'border-slate-300'}`}>
                  {selectedDessert === opt && <div className="w-2.5 h-2.5 bg-brand-primary rounded-full"></div>}
                </div>
                <span className="font-medium text-slate-700">{opt}</span>
              </label>
            ))}
          </div>
        </div>

      </div>

      {/* Checkout inferior dedicado al Menú */}
      <div className="mt-8 flex flex-col md:flex-row items-center justify-between p-6 bg-slate-900 rounded-2xl shadow-xl">
         <div className="mb-4 md:mb-0">
             <span className="block text-slate-400 text-sm">Total del Menú Completado</span>
             <span className="text-white font-bold text-2xl font-display">15.00€</span>
         </div>
         <button 
           onClick={handleAddMenu}
           className="w-full md:w-auto bg-brand-accent hover:bg-yellow-500 disabled:opacity-50 disabled:bg-slate-700 text-slate-900 disabled:text-slate-400 px-10 py-4 rounded-xl font-bold text-lg transition-colors cursor-pointer"
           disabled={!isMenuSelected}
         >
           {isMenuSelected ? 'Añadir Menú al Pedido' : 'Selecciona las 3 opciones'}
         </button>
      </div>

    </div>
  );
};

export default DailyMenuView;
