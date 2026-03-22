import React from "react";
import type { Order } from "../api/orders";

type Props = {
  orders: Order[];
};

export default function OrderList({ orders }: Props) {
  return (
    <div>
      <h2>Pedidos</h2>

      {orders.length === 0 ? (
        <p>Nenhum pedido encontrado.</p>
      ) : (
        <ul>
          {orders.map((order) => (
            <li key={order.id}>
              <strong>#{order.id}</strong> — {order.customer_name} | {order.product} | qtd:{" "}
              {order.quantity} | status: {order.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}