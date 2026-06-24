#include <Arduino.h>

// --- 电机物理模型参数 ---
float Ku = 1.5; // 输入增益常数
float Kw = 0.5; // 反电动势/阻尼常数
float current_omega = 0.0; // 当前角速度

// --- PI 控制器参数 ---
float Kp = 2.0; // 比例系数
float Ki = 5.0; // 积分系数
float integral = 0.0; // 积分累积量

unsigned long last_time = 0;

// 软件模拟直流电机模型：dω/dt = (Ku·u − Kw·ω)
float update_motor_model(float u, float dt_sec) {
    float d_omega = (Ku * u) - (Kw * current_omega);
    current_omega += d_omega * dt_sec;
    return current_omega;
}

// PI 闭环控制器
float compute_pi(float setpoint, float measured_value, float dt_sec) {
    float error = setpoint - measured_value;
    integral += error * dt_sec;
    
    float output = (Kp * error) + (Ki * integral);
    
    // Anti-windup 积分限幅 (假设输出范围是 -100 到 100)
    if (output > 100.0) output = 100.0;
    if (output < -100.0) output = -100.0;
    
    return output;
}

void setup() {
    // 初始化串口，波特率 115200
    Serial.begin(115200);
    delay(1000); 
    last_time = millis();
}

void loop() {
    unsigned long current_time = millis();
    
    // 设定控制周期为 10ms (100Hz)
    if (current_time - last_time >= 10) { 
        float dt_sec = (current_time - last_time) / 1000.0;
        last_time = current_time;

        // 给定一个阶跃目标速度：50.0 rad/s
        float target_velocity = 50.0; 
        
        // 1. 计算控制信号 u
        float control_signal = compute_pi(target_velocity, current_omega, dt_sec);
        
        // 2. 将控制信号输入电机模型，获取新的实际速度
        current_omega = update_motor_model(control_signal, dt_sec);

        // 3. 通过 UART 发送遥测数据 (格式: 时间, 目标速度, 实际速度)
        Serial.print(current_time);
        Serial.print(",");
        Serial.print(target_velocity);
        Serial.print(",");
        Serial.println(current_omega);
    }
}