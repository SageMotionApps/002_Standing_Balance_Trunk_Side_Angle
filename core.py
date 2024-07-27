import logging
from sage.base_app import BaseApp

if __name__ == "__main__":
    from Quaternion import Quaternion
else:
    from .Quaternion import Quaternion


class Core(BaseApp):

    ###########################################################
    # INITIALIZE APP
    ###########################################################
    def __init__(self, my_sage):
        BaseApp.__init__(self, my_sage, __file__)

        self.iteration = 0
        self.current_quat = Quaternion()

        # The prefix "self" denotes global variables
        # get values from web interface [NOTE: add negative sign for left and back]
        self.max_lean_right = self.config["max_lean_right"]
        self.max_lean_left = -self.config["max_lean_left"]

        # Define the node number for sensing
        self.NodeNum_trunk = self.info["sensors"].index("trunk")

        # Define the node numbers for feedback
        self.right_feedback_nodeNum = self.info["feedback"].index("right feedback")
        self.left_feedback_nodeNum = self.info["feedback"].index("left feedback")

        # Default to zero in case feedback is disabled
        self.right_feedback_state = 0
        self.left_feedback_state = 0

    ###########################################################
    # CHECK NODE CONNECTIONS
    ###########################################################
    def check_status(self):
        # check if the requirement if satisfied
        sensors_count = self.get_sensors_count()
        feedback_count = self.get_feedback_count()
        logging.debug("config pulse length {}".format(self.info["pulse_length"]))
        err_msg = ""
        if sensors_count < len(self.info["sensors"]):
            err_msg += "App requires {} sensors but only {} are connected".format(
                len(self.info["sensors"]), sensors_count
            )
        if self.config["feedback_enabled"] and feedback_count < len(
            self.info["feedback"]
        ):
            err_msg += "App require {} feedback but only {} are connected".format(
                len(self.info["feedback"]), feedback_count
            )
        if err_msg != "":
            return False, err_msg
        return True, "Now running Standing Balance Side Angle App"

    #############################################################
    # UPON STARTING THE APP
    # If you have anything that needs to happen before the app starts
    # collecting data, you can uncomment the following lines
    # and add the code in there. This function will be called before the
    # run_in_loop() function below.
    #############################################################
    # def on_start_event(self, start_time):
    #     print("In On Start Event: {start_time}")

    ###########################################################
    # RUN APP IN LOOP
    ###########################################################
    def run_in_loop(self):
        # Get next data packet
        data = self.my_sage.get_next_data()

        # Get Quaternion Data
        self.current_quat.updateFromRawData(data=data[self.NodeNum_trunk])

        # Calculate the Trunk Side Angle (TSA)
        TSA = self.current_quat.TrunkSwayAngle()

        # Turn feedback nodes on/off
        if self.config["feedback_enabled"]:
            self.give_feedback(TSA)

        time_now = self.iteration / self.info["datarate"]  # time in seconds

        # To save data, add it to the my_data structure and update the user_fields in info.json accordingly
        my_data = {
            "time": [time_now],
            "TSA": [TSA],
            "max_lean_right": [self.max_lean_right],
            "max_lean_left": [self.max_lean_left],
            "right_feedback_state": [self.right_feedback_state],
            "left_feedback_state": [self.left_feedback_state],
        }

        self.my_sage.save_data(data, my_data)
        self.my_sage.send_stream_data(data, my_data)

        # Increment and save data
        self.iteration += 1

        return True

    #############################################################
    # MANAGE FEEDBACK FOR APP
    #############################################################
    def toggle_feedback(self, feedbackNode=0, duration=1, feedback_state=False):
        if feedback_state:
            self.my_sage.feedback_on(feedbackNode, duration)
        else:
            self.my_sage.feedback_off(feedbackNode)

    def give_feedback(self, TSA):

        pulse_length = self.info["pulse_length"]
        self.right_feedback_state = int(TSA > self.max_lean_right)
        self.left_feedback_state = int(TSA < self.max_lean_left)

        # Give feedback for TSA (using push feedback paradigm)
        self.toggle_feedback(
            self.right_feedback_nodeNum,
            duration=pulse_length,
            feedback_state=self.right_feedback_state,
        )
        self.toggle_feedback(
            self.left_feedback_nodeNum,
            duration=pulse_length,
            feedback_state=self.left_feedback_state,
        )

    #############################################################
    # UPON STOPPING THE APP
    # If you have anything that needs to happen after the app stops,
    # you can uncomment the following lines and add the code in there.
    # This function will be called after the data file is saved and
    # can be read back in for reporting purposes if needed.
    #############################################################
    # def on_stop_event(self, stop_time):
    #     print(f"In On Stop Event: {stop_time}")
