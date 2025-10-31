import os
import json

class TextSymbolAssociation:
    def __init__(self, image_path, text_boxes, symbol_boxes,query=None):
        self.image_path = image_path 
        self.text_boxes = text_boxes
        self.symbol_boxes = symbol_boxes
        self.query = query
    def associate_text_to_symbol(image_path, text_boxes, symbol_boxes, distance_threshold=50 ):
        associations = []

        for t_box in text_boxes:
            tx,ty = t_box['center']

            closest_symbol = None
            min_distance = float('inf')

            for s_box in symbol_boxes:
                sx,sy = s_box['center']
                distance = ((tx-sx)**2 +(ty-sy)**2)**0.5

                if distance < min_distance and distance < distance_threshold:
                    min_distance = distance
                    closest_symbol = s_box['id']
                    symbol_bbox = s_box['bbox']
                    symbol_center = s_box['center']

            if closest_symbol is not None:
                associations.append({
                    'text_id': t_box['id'],
                    'text_center': t_box['center'],
                    'symbol_id': closest_symbol,
                    'symbol_bbox':symbol_bbox,
                    'symbol_center': symbol_center,
                    'distance': round(min_distance, 2)
                })

        with open(f"{os.path.basename(image_path).split('.')[0]}_associations.json", "w") as f:
            json.dump(associations, f, indent=4)
        return associations
    def association_query(self,text_symbol_association, symbol_box, query=None):
        if query is not None:
            #If full text metadata is provided
            if isinstance(query, dict):  
                text_id = query.get('id')
            else: 
                #If only text id is given 
                text_id = query

            for assoc in text_symbol_association:
                if assoc['text_id'] == text_id:
                    # Return full symbol metadata
                    return next((s for s in symbol_box if s['id'] == assoc['symbol_id']), None)
    def process(self):
        print("In Extaracted Components")
        txt_sym_association = self.associate_text_to_symbol(self.image_path, self.text_boxes,self.symbol_boxes)
        if self.query is not None:
            mapped_symbol = self.association_query(txt_sym_association, self.symbol_boxes, self.query)
        else:
            mapped_symbol= []
        return txt_sym_association, mapped_symbol