export type Order = {
  id: number;
  customer_name: string;
  product: string;
  quantity: number;
  status: string;
  created_at: string;
};

const BASE_URL = "http://localhost:8002/orders";

export async function fetchOrders(status?: string): Promise<Order[]> {
  const url = status ? `${BASE_URL}/?status=${status}` : `${BASE_URL}/`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch orders");
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
    throw new Error("Failed to create order");
  }

  return response.json();
}