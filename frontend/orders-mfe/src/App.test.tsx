import { render } from "@testing-library/react";
import App from "./App";
import "@testing-library/jest-dom";

describe("App", () => {
  it("should be in the document", () => {
    const { getByText } = render(<App name="Testapp" />);
    expect(getByText(/Testapp is mounted!/i)).toBeInTheDocument();
  });
});
