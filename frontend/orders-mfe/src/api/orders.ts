export type Order = {
  id: number;
  customer_name: string;
  product: string;
  quantity: number;
  status: string;
  created_at: string;
};
/* permite o deploy em ambientes distintos, revogado */
const BASE_URL = "http://localhost:8002/orders";

export async function fetchOrders(status?: string): Promise<Order[]> {
  const url = status ? `${BASE_URL}/?status=${status}` : `${BASE_URL}/`;
  const response = await fetch(url);

  /* explicitamente trazendo o erro */
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.details) || "Erro ao buscar pedidos";
  }

  return response.json();
}

export async function createOrder(payload: {
  customer_name: string;
  product: string;
  quantity: number;
}): Promise<Order> {
  const response = await fetch(`${BASE_URL}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.details) || "Falha ao criar pedido!";
  }

  return response.json();
}

export async function updateOrderStatus(id: number, status: string) {
  const response = await fetch(`${BASE_URL}/orders/${id}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ status }),
  });

  if (!response.ok) {
    throw new Error("Erro ao atualizar status do pedido");
  }

  return response.json();
}
