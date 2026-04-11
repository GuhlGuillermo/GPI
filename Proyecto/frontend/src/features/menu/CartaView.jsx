import React from 'react';
import DishCard from './components/DishCard';
import ShoppingCart from '../cart/components/ShoppingCart';

const CartaView = ({ cartItems, setCartItems, onAdd }) => {
  return (
    <div className="flex flex-col lg:flex-row gap-12">
        {/* Zona de Catálogo (Grid Dinámico Disperso) */}
        <div className="flex-1 animate-fade-in">
          <h2 className="text-4xl font-display font-black text-brand-dark mb-2">Nuestra Carta</h2>
          <p className="text-slate-500 mb-8 border-b border-slate-200 pb-4">Elige tus platos favoritos de forma individual.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <DishCard onAdd={onAdd} dish={{ dish_id: 'D1', name: 'Momo de Pollo', description: 'Empanadillas caseras de pollo y especias echas al vapor.', snapshot_price: 6.50, category: 'Entrantes' }} />
            <DishCard onAdd={onAdd} dish={{ dish_id: 'D2', name: 'Pollo Tikka Masala', description: 'Trozos de pollo bañados en cremosa y dulce salsa.', snapshot_price: 14.50, category: 'Principal' }} />
            <DishCard onAdd={onAdd} dish={{ dish_id: 'D3', name: 'Pan Naan Queso', description: 'Pan tradicional plano cocinado en horno de barro relleno de queso fundido.', snapshot_price: 4.00, category: 'Acompañamiento' }} />
            <DishCard onAdd={onAdd} dish={{ dish_id: 'D4', name: 'Lassi de Mango', description: 'Batido de yogur natural agridulce y pulpa de mango puro.', snapshot_price: 3.50, category: 'Bebidas' }} />
          </div>
        </div>

        {/* Zona Lateral del checkout */}
        <aside className="w-full lg:w-[400px]">
          <div className="sticky top-28">
            <ShoppingCart items={cartItems} setItems={setCartItems}/>
          </div>
        </aside>
    </div>
  );
};

export default CartaView;
