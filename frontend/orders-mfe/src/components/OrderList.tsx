import React, { useEffect, useState } from "react";
import type { Order } from "../api/orders";
import { updateOrderStatus } from "../api/orders";

type Props = {
  orders: Order[];
  onStatusUpdated?: () => Promise<void> | void;
};

export default function OrderList({ orders, onStatusUpdated }: Props) {
  const [localOrders, setLocalOrders] = useState<Order[]>(orders);

  useEffect(() => {
    setLocalOrders(orders);
  }, [orders]);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);

  const handleStatusChange = async (orderId: number, newStatus: string) => {
    try {
      const updatedOrder = await updateOrderStatus(orderId, newStatus);

      setLocalOrders((currentOrders) =>
        currentOrders.map((order) =>
          order.id === orderId ? { ...order, ...updatedOrder } : order
        )
      );

      if (onStatusUpdated) {
        await onStatusUpdated();
      }
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
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>ID</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Cliente</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Produto</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Qtd</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Preço</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Total</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {localOrders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td>{order.customer_name}</td>
                <td>{order.product}</td>
                <td>{order.quantity}</td>
                <td>{formatCurrency(order.price)}</td>
                <td>{formatCurrency(order.quantity * order.price)}</td>
                <td>
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
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}