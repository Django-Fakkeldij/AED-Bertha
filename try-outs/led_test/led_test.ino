// Declare global variables
int current_pos[2] = {0, 0};
int x_array[] = {200, 0, -200};
int y_array[] = {-100, 50, 200};
int array_length = sizeof(x_array) / sizeof(x_array[0]);

// Function prototypes
void move_to(int x, int y, int* stored_pos);
void full_movement(int* x_arr, int* y_arr, int arr_len);

void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(115200);
  // Execute the full movement function
  full_movement(x_array, y_array, array_length);
}

void loop() {
  // Nothing to do here
}

void move_to(int x, int y, int* stored_pos) {
  // Calculate actuated steps
  int actuated_steps[2];
  actuated_steps[0] = x - stored_pos[0];
  actuated_steps[1] = y - stored_pos[1];
  
  // // Create movement string
  // String movement = String(actuated_steps[0]) + "," + String(actuated_steps[1]);
  
  // // Send movement command via Serial
  // Serial.println(movement);
  
  // Update current position
  stored_pos[0] += actuated_steps[0];
  stored_pos[1] += actuated_steps[1];
}

void full_movement(int* x_arr, int* y_arr, int arr_len) {
  for (int i = 0; i < arr_len; i++) {
    move_to(x_arr[i], y_arr[i], current_pos);
    delay(5000);  // Pause for 5 seconds between movements
  }
}

full_movement({200, 0, -200},{-100, 50, 200});
