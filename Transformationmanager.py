import json
from Transformation_Class import Transformation
from Labels_Class import Labels
from out_of_bounds import Out_of_bounds

class TransManager():
    def __init__(self):
        self.transformations = [] #list of transformation instances
        self.labels = []    #list of label instances
        self.out_of_bounds_instances = [] #list of out_of_bounds instances
        self.load_state()

    def add_transformation(self):
        """
        Adds a new transformation instance to the transformation list
        """
        transformation = Transformation()
        self.transformations.append(transformation)
        label = Labels(transformation)
        self.labels.append(label)
        out_of_bounds_instance = Out_of_bounds()
        self.out_of_bounds_instances.append(out_of_bounds_instance)
        self.save_state()

    def create_calibration_file(self, lines):
        """
        Writes the list of 4 stage-corner coordinates to a new Calibration_x.txt file
        """
        filename = f"Calibration_{len(self.transformations)}.txt"
        with open(filename, 'w') as file:
            print(lines)
            for line in lines:
                line = str(line) + "\n"
                file.write(line)
            # Write initial corner values or other relevant data

    def update_all_labels(self):
        """
        Calls the update_labels() function of the Labels() Class for all label instances
        """
        for label in self.labels:
            label.update_labels()

    def check_out_of_bounds(self):
        """
        Calls the out_of_bounds() function of the Out_of_bounds() Class for all out_of_bounds instances
        """
        for i, transformation in enumerate(self.transformations):
            pan = transformation.get_cart_pan()
            tilt = transformation.get_cart_tilt()
            out_of_bounds_instance = self.out_of_bounds_instances[i]
            out_of_bounds_instance.check(pan, tilt)


    def save_state(self):
        """
        Saves the state of the transformations to a JSON file
        """
        state = {
            "transformations": len(self.transformations)
        }
        with open('state.json', 'w') as file:
            json.dump(state, file)

    def load_state(self):
        """
        Loads the state of the transformations from a JSON file
        """
        try:
            with open('state.json', 'r') as file:
                state = json.load(file)
                for _ in range(state["transformations"]):
                    self.add_transformation()
        except FileNotFoundError:
            pass

    def delete_transformation(self, index):
        """
        Deletes a specific transformation instance by its index
        """
        if 0 <= index < len(self.transformations):
            del self.transformations[index]
            del self.labels[index]
            del self.out_of_bounds_instances[index]
            self.save_state()

transmanager = TransManager()