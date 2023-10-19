import "@testing-library/jest-dom";
import { screen, render, fireEvent, waitFor } from "@testing-library/react";
import App from "./App";

describe("App", () => {
  beforeEach(() => {
    jest.spyOn(global, "fetch").mockResolvedValue({
      json: jest.fn().mockResolvedValue({
        data: {
          id: "id",
          title: "title",
          clones: [],
        },
      }),
    } as unknown as Response);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  // There isn't much to test since it uses a canvas element it's not possible
  // to dive into it and make assertions based on it.
  test("renders the canvas", async () => {
    const { container } = render(<App />);

    // There should be a load button.
    const loadJourneys = screen.queryByRole("button", {
      name: "Load Journeys",
    });
    expect(loadJourneys).toBeInTheDocument();

    // After clicking on it, the canvas should load
    fireEvent.click(loadJourneys);

    // Wait for the canvas to render.
    await waitFor(() => {
      expect(container.querySelectorAll("canvas").length).toBeGreaterThan(0);
    });

    // The load button has disappeared.
    expect(loadJourneys).not.toBeInTheDocument();
  });
});
