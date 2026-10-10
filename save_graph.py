"""
Save the compiled LangGraph (travel_graph) to your folder.
Generates:
  - travel_graph.png  (image)
  - travel_graph.mmd  (mermaid text fallback)
Run: python save_graph.py
"""
import os

# Try to import the already-compiled graph from backend.py
# This will also try to connect to Postgres - if that fails we rebuild graph without DB
try:
    from backend import travel_graph
    print("Loaded travel_graph from backend.py")
except Exception as e:
    print(f"Could not load from backend.py (DB issue?): {e}")
    print("Rebuilding graph without checkpointer for visualization...")
    from langgraph.graph import StateGraph, START, END
    from backend import TravelState, flight_agent, hotel_agent, itinerary_agent, final_agent

    graph = StateGraph(TravelState)
    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("final_agent", final_agent)
    graph.add_edge(START, "flight_agent")
    graph.add_edge("flight_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", "final_agent")
    graph.add_edge("final_agent", END)
    travel_graph = graph.compile()
    print("Rebuilt graph without checkpointer")

# --- 1. Save Mermaid text (always works, no extra deps) ---
try:
    mermaid_text = travel_graph.get_graph().draw_mermaid()
    with open("travel_graph.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_text)
    print("✅ Saved: travel_graph.mmd")
    print(mermaid_text)
except Exception as e:
    print(f"❌ Failed to save .mmd: {e}")

# --- 2. Save ASCII (for terminal view) ---
try:
    ascii_text = travel_graph.get_graph().draw_ascii()
    with open("travel_graph.txt", "w", encoding="utf-8") as f:
        f.write(ascii_text)
    print("\n✅ Saved: travel_graph.txt")
    print(ascii_text)
except Exception as e:
    print(f"❌ Failed to save .txt: {e}")

# --- 3. Save PNG image (requires internet to hit mermaid.ink) ---
try:
    png_bytes = travel_graph.get_graph().draw_mermaid_png()
    with open("travel_graph.png", "wb") as f:
        f.write(png_bytes)
    print("\n✅ Saved: travel_graph.png")
except Exception as e:
    print(f"\n⚠️ Could not save PNG via draw_mermaid_png: {e}")
    print("Fallback: You can paste travel_graph.mmd into https://mermaid.live to export PNG manually.")
    # Try alternative draw_png if graphviz is installed
    try:
        png_bytes = travel_graph.get_graph().draw_png()
        with open("travel_graph_alt.png", "wb") as f:
            f.write(png_bytes)
        print("✅ Saved alternative: travel_graph_alt.png")
    except Exception as e2:
        print(f"Alternative PNG also failed: {e2}")
