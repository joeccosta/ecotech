import React, { useEffect, useState } from "react";
import type { Order } from "../api/orders";
import { updateOrderStatus } from "../api/orders";

type Props = {
  orders: Order[];
};

export default function OrderList({ orders }: Props) {
  const [localOrders, setLocalOrders] = useState<Order[]>(orders);

  useEffect(() => {
    setLocalOrders(orders);
  }, [orders]);

  const handleStatusChange = async (orderId: number, newStatus: string) => {
    try {
      const updatedOrder = await updateOrderStatus(orderId, newStatus);

      setLocalOrders((currentOrders) =>
        currentOrders.map((order) =>
          order.id === orderId ? { ...order, ...updatedOrder } : order
        )
      );
    } catch (error) {
      console.error("Erro ao atualizar status do pedido:", error);
      alert("Não foi possível atualizar o status do pedido.");
    }
  };

  return (
    <div>
      <h2>Pedidos</h2>

      {localOrders.length === 0 ? (
        <p>Nenhum pedido encontrado.</p>
      ) : (
        <ul>
          {localOrders.map((order) => (
            <li key={order.id}>
              <strong>#{order.id}</strong> — {order.customer_name} | {order.product} | qtd:{" "}
              {order.quantity} |{" "}
              <label>
                status:{" "}
                <select
                  value={order.status}
                  onChange={(e) => handleStatusChange(order.id, e.target.value)}
                >
                  <option value="pending">pending</option>
                  <option value="processing">processing</option>
                  <option value="shipped">shipped</option>
                  <option value="delivered">delivered</option>
                  <option value="cancelled">cancelled</option>
                </select>
              </label>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}