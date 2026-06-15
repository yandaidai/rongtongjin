import React, { useEffect, useRef, useState } from 'react';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import {
  Alert, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text,
  TextInput, TouchableOpacity, View,
} from 'react-native';
import { useAuth } from '../store/AuthContext';

type LoginNavProp = NativeStackNavigationProp<Record<string, undefined>, 'Login'>;

export default function LoginScreen({ navigation }: { navigation: LoginNavProp }) {
  const { login } = useAuth();
  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // 组件卸载时清除倒计时定时器，防止内存泄漏
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, []);

  const sendCode = () => {
    if (phone.length < 10) {
      Alert.alert('提示', '请输入正确的手机号');
      return;
    }
    // 生产环境：调用真实短信接口
    Alert.alert('提示', `验证码已发送至 ${phone}（开发环境固定 123456）`);
    setCountdown(60);
    timerRef.current = setInterval(() => {
      setCountdown((c) => {
        if (c <= 1) {
          if (timerRef.current) {
            clearInterval(timerRef.current);
            timerRef.current = null;
          }
          return 0;
        }
        return c - 1;
      });
    }, 1000);
  };

  const handleLogin = async () => {
    if (!phone || !code) {
      Alert.alert('提示', '请填写手机号和验证码');
      return;
    }
    setLoading(true);
    try {
      await login(phone, code);
    } catch (e: unknown) {
      Alert.alert('登录失败', e instanceof Error ? e.message : '未知错误');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
        <View style={styles.header}>
          <Text style={styles.logo}>融通金</Text>
          <Text style={styles.subtitle}>黄金回收交易平台</Text>
        </View>

        <View style={styles.form}>
          <Text style={styles.label}>手机号</Text>
          <TextInput
            style={styles.input}
            placeholder="请输入手机号"
            keyboardType="phone-pad"
            maxLength={15}
            value={phone}
            onChangeText={setPhone}
          />

          <Text style={styles.label}>验证码</Text>
          <View style={styles.codeRow}>
            <TextInput
              style={[styles.input, styles.codeInput]}
              placeholder="请输入验证码"
              keyboardType="number-pad"
              maxLength={6}
              value={code}
              onChangeText={setCode}
            />
            <TouchableOpacity
              style={[styles.codeBtn, countdown > 0 && styles.codeBtnDisabled]}
              onPress={sendCode}
              disabled={countdown > 0}
            >
              <Text style={[styles.codeBtnText, countdown > 0 && styles.codeBtnTextDisabled]}>
                {countdown > 0 ? `${countdown}s` : '获取验证码'}
              </Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.submitBtn, loading && styles.submitBtnDisabled]}
            onPress={handleLogin}
            disabled={loading}
          >
            <Text style={styles.submitText}>{loading ? '登录中...' : '登录'}</Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={() => navigation.navigate('Register')}>
            <Text style={styles.link}>没有账号？立即注册</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  scroll: { flexGrow: 1, justifyContent: 'center', padding: 24 },
  header: { alignItems: 'center', marginBottom: 40 },
  logo: { fontSize: 36, fontWeight: '800', color: '#d4a84b' },
  subtitle: { fontSize: 14, color: '#999', marginTop: 4 },
  form: { backgroundColor: '#fff', borderRadius: 16, padding: 24, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 12, elevation: 3 },
  label: { fontSize: 14, fontWeight: '600', color: '#333', marginBottom: 6, marginTop: 12 },
  input: { borderWidth: 1, borderColor: '#e0e0e0', borderRadius: 10, padding: 14, fontSize: 16, backgroundColor: '#fafafa' },
  codeRow: { flexDirection: 'row', gap: 10 },
  codeInput: { flex: 1 },
  codeBtn: { backgroundColor: '#d4a84b', borderRadius: 10, paddingHorizontal: 16, justifyContent: 'center' },
  codeBtnDisabled: { backgroundColor: '#ccc' },
  codeBtnText: { color: '#fff', fontWeight: '600', fontSize: 14 },
  codeBtnTextDisabled: { color: '#fff' },
  submitBtn: { backgroundColor: '#d4a84b', borderRadius: 10, padding: 16, alignItems: 'center', marginTop: 24 },
  submitBtnDisabled: { opacity: 0.6 },
  submitText: { color: '#fff', fontSize: 18, fontWeight: '700' },
  link: { textAlign: 'center', color: '#d4a84b', marginTop: 16, fontSize: 14 },
});
