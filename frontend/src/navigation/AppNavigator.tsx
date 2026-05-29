import React from 'react';
import { ActivityIndicator, Text, View } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NavigationContainer } from '@react-navigation/native';
import { useAuth } from '../store/AuthContext';

import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import ProductsScreen from '../screens/ProductsScreen';
import DomesticQuotesScreen from '../screens/DomesticQuotesScreen';
import InternationalQuotesScreen from '../screens/InternationalQuotesScreen';
import KlineScreen from '../screens/KlineScreen';
import ProfileScreen from '../screens/ProfileScreen';
import SpreadConfigScreen from '../screens/SpreadConfigScreen';
import WarnListScreen from '../screens/WarnListScreen';
import WarnCreateScreen from '../screens/WarnCreateScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const TAB_ICONS: Record<string, string> = {
  ProductsTab: '📊',
  DomesticTab: '🇨🇳',
  InternationalTab: '🌍',
  ProfileTab: '👤',
};

function TabIcon({ routeName, focused }: { routeName: string; focused: boolean }) {
  return (
    <Text style={{ fontSize: focused ? 24 : 20, opacity: focused ? 1 : 0.6 }}>
      {TAB_ICONS[routeName] || '📄'}
    </Text>
  );
}

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused }) => <TabIcon routeName={route.name} focused={focused} />,
        tabBarActiveTintColor: '#d4a84b',
        tabBarInactiveTintColor: '#999',
        tabBarStyle: {
          backgroundColor: '#fff',
          borderTopWidth: 1,
          borderTopColor: '#f0f0f0',
          paddingBottom: 6,
          paddingTop: 6,
          height: 56,
        },
        tabBarLabelStyle: { fontSize: 11, fontWeight: '600' },
        headerStyle: { backgroundColor: '#d4a84b' },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: '700' },
      })}
    >
      <Tab.Screen
        name="ProductsTab"
        component={ProductsScreen}
        options={{ title: '产品价格', tabBarLabel: '首页' }}
      />
      <Tab.Screen
        name="DomesticTab"
        component={DomesticQuotesScreen}
        options={{ title: '国内大盘', tabBarLabel: '国内' }}
      />
      <Tab.Screen
        name="InternationalTab"
        component={InternationalQuotesScreen}
        options={{ title: '国际大盘', tabBarLabel: '国际' }}
      />
      <Tab.Screen
        name="ProfileTab"
        component={ProfileScreen}
        options={{ title: '我的', tabBarLabel: '我的' }}
      />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#f5f5f5' }}>
        <ActivityIndicator size="large" color="#d4a84b" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: '#d4a84b' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: '700' },
        }}
      >
        {isAuthenticated ? (
          <>
            <Stack.Screen name="Main" component={MainTabs} options={{ headerShown: false }} />
            <Stack.Screen
              name="Kline"
              component={KlineScreen}
              options={({ route }: any) => ({ title: route.params?.productName || 'K线图' })}
            />
            <Stack.Screen name="SpreadConfig" component={SpreadConfigScreen} options={{ title: '点差配置' }} />
            <Stack.Screen name="WarnList" component={WarnListScreen} options={{ title: '价格预警' }} />
            <Stack.Screen
              name="WarnCreate"
              component={WarnCreateScreen}
              options={({ route }: any) => ({ title: route.params?.warnId ? '编辑预警' : '新建预警' })}
            />
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen
              name="Register"
              component={RegisterScreen}
              options={{
                title: '注册',
                headerStyle: { backgroundColor: '#fff' },
                headerTintColor: '#1a1a2e',
              }}
            />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
