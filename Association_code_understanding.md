# Text-to-Symbol Association Module

## Overview

This module defines a class **`TextSymbolAssociation`** that creates associations between detected text regions and symbol regions in an engineering or P&ID diagram image.

It identifies the closest symbol for each detected text block based on Euclidean distance and saves:

* A **JSON file** describing associations (`text_id → symbol_id`)


---

## Dependencies

Ensure the following libraries are installed:

```bash
pip install numpy
```

---

## Class: `TextSymbolAssociation`

### Purpose

To link text annotations to the nearest graphical symbols in a diagram using their spatial coordinates.

---

## Input

### Constructor Parameters

| Parameter      | Type                                   | Description                                                                                                  |
| -------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------
|`image_path`    |  str                                   | Simply for naming json file
| `text_boxes`   | list[dict]                             | List of text metadata dictionaries (see below).                                                              |
| `symbol_boxes` | list[dict]                             | List of symbol metadata dictionaries (see below).                                                            |
| `query`        | bool or dict (optional, default=False) | Used for querying association results. If `True` or provided with a dict, enables query-based symbol lookup. |

---

### Input Metadata Formats

#### Text Metadata Format

Each entry in `text_boxes` should follow this structure:

```json
{
    "id": "T1",
    "text": "Valve 101",
    "coordinates": [(x1, y1), (x2, y2), (x3, y3), (x4, y4)],
    "orientation": 0,
    "center": (cx, cy)
}
```

| Key           | Description                                  |
| ------------- | -------------------------------------------- |
| `id`          | Unique text identifier.                      |
| `text`        | The extracted text content.                  |
| `coordinates` | Bounding box coordinates of the text region. |
| `orientation` | Detected rotation angle of the text.         |
| `center`      | Center point (cx, cy) of the text region.    |

#### Symbol Metadata Format

Each entry in `symbol_boxes` should follow this structure:

```json
{
    "id": "S1",
    "shape": "circle",
    "bbox": [x, y, x+w, y+h],
    "center": (cx, cy)
}
```

| Key      | Description                                           |
| -------- | ----------------------------------------------------- |
| `id`     | Unique symbol identifier.                             |
| `shape`  | Detected symbol type (e.g., circle, rectangle, etc.). |
| `bbox`   | Bounding box coordinates of the symbol.               |
| `center` | Center point (cx, cy) of the symbol region.           |

---

## Output

| Output           | Type         | Description                                                                                     |
| ---------------- | ------------ | ----------------------------------------------------------------------------------------------- |
| **Returns**      | list[dict]   | List of text-symbol association objects.                                                        |
| **Generates**    | `.json` file | Stores association details between text and symbols.                                            |
| **Query Output** | dict or None | When using `association_query()`, returns the symbol metadata corresponding to a given text ID. |

---

## Example Output JSON (`*_associations.json`)

```json
[
    {
        "text_id": "T1",
        "text_center": [320, 220],
        "symbol_id": "S2",
        "symbol_center": [340, 250],
        "distance": 31.24
    },
    {
        "text_id": "T2",
        "text_center": [500, 150],
        "symbol_id": "S3",
        "symbol_center": [520, 180],
        "distance": 36.4
    }
]
```

---

## Method Details

### `associate_text_to_symbol()`

Associates each text box with the closest symbol within a specified distance threshold.

| Name                 | Type       | Default | Description                               |
| -------------------- | ---------- | ------- | ----------------------------------------- |
| `text_boxes`         | list[dict] | —       | List of text metadata dictionaries.       |
| `symbol_boxes`       | list[dict] | —       | List of symbol metadata dictionaries.     |
| `distance_threshold` | int        | 50      | Maximum allowed distance for association. |

#### Logic

For each text box:

1. Compute the Euclidean distance to every symbol.
2. Select the closest symbol within the `distance_threshold`.
3. Create an association record containing:

   * Text and Symbol IDs
   * Their centers
   * The computed distance
4. Save:

   * Association data (`*_associations.json`)


---

### `association_query()`

Retrieves the associated symbol metadata for a given text ID from precomputed text-symbol associations.

| Name                      | Type                | Default | Description                                        |
| ------------------------- | ------------------- | ------- | -------------------------------------------------- |
| `text_symbol_association` | list[dict]          | —       | List of existing text-symbol association mappings. |
| `symbol_box`              | list[dict]          | —       | Full list of symbol metadata.                      |
| `query`                   | str or dict or None | None    | Text ID or metadata to query.                      |

#### Logic

1. If a `query` is provided:

   * If it’s a dictionary, extract `text_id` using `query.get('id')`.
   * Otherwise, treat `query` as the text ID directly.
2. Loop through the `text_symbol_association` list to find a matching `text_id`.
3. Return the corresponding **symbol metadata** by matching the `symbol_id` in the `symbol_box` list.
4. If no match is found, return `None`.

#### Example

```python
symbol_info = assoc.association_query(text_symbol_association, symbol_metadata, query="T2")
print(symbol_info)
```

**Output Example**

```json
{
    "id": "S3",
    "shape": "rectangle",
    "bbox": [120, 210, 160, 250],
    "center": [140, 230]
}
```

---

### `process()`

Wrapper function to trigger the text-symbol association process.

#### Logic Flow

1. Prints a message indicating the start of processing.
2. Calls `associate_text_to_symbol()` internally.
3. Returns the generated association list.

---

## Example Usage

```python
from text_symbol_association import TextSymbolAssociation

# Example text and symbol metadata
text_metadata = [
    {"id": "T1", "text": "Valve 101", "coordinates": [(10,10),(80,10),(80,40),(10,40)], "orientation": 0, "center": (45,25)},
    {"id": "T2", "text": "Pump A", "coordinates": [(100,200),(180,200),(180,230),(100,230)], "orientation": 0, "center": (140,215)}
]

symbol_metadata = [
    {"id": "S1", "shape": "circle", "bbox": [60, 20, 100, 60], "center": (80,40)},
    {"id": "S2", "shape": "rectangle", "bbox": [120, 210, 160, 250], "center": (140,230)}
]

# Initialize and process
assoc = TextSymbolAssociation(image_path, text_metadata, symbol_metadata)
result = assoc.process()

# Query for a specific text-to-symbol mapping
symbol_info = assoc.association_query(result, symbol_metadata, query="T1")
print(symbol_info)
```

---

## Output Files

| File                             | Description                                    |
| -------------------------------- | ---------------------------------------------- |
| `diagram_associations.json`      | Stores text-symbol connection metadata.        |
---
