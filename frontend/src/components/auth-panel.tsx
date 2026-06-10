import { useState } from "react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { useNavigate } from "react-router-dom"
import { Header } from "./header"
import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
export function AuthPanel() {
  const [mode, setMode] = useState<"login" | "register">("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [errors, setErrors] = useState<Record<string, string>>({})
  const navigate = useNavigate()
  
  const validate = () => {
    const newErrors: Record<string, string> = {}
    
    if (!email) {
      newErrors.email = "El correo es obligatorio"
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Formato de correo inválido"
    }
    
    if (!password) {
      newErrors.password = "La contraseña es obligatoria"
    } else if (password.length < 6) {
      newErrors.password = "La contraseña debe tener al menos 6 caracteres"
    }
    
    if (mode === "register") {
      if (!confirmPassword) {
        newErrors.confirmPassword = "Debes confirmar la contraseña"
      } else if (password !== confirmPassword) {
        newErrors.confirmPassword = "Las contraseñas no coinciden"
      }
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

 const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  if (validate()) {
    const endpoint = mode === "login" ? "/login" : "/register";
    const response= await axios.post(`${API_URL}${endpoint}`, { email, password });
    if (response.status === 200) {
       
      localStorage.setItem("userEmail", response.data.email); // Guardar identificador
      navigate("/search");
    } else {
      setErrors({ email: "Error en la autenticación" });
    }
  }
};

  return (
    <div className="relative flex flex-col min-h-svh w-full bg-background font-sans antialiased items-center justify-center p-4">
      <Header />
      <div className="w-full max-w-md p-8 border border-border/40 bg-background/50 backdrop-blur-md rounded-2xl shadow-lg mt-16 animate-in fade-in zoom-in-95 duration-500">
        <div className="flex flex-col items-center mb-8">
          <h2 className="text-2xl font-bold tracking-tight">
            {mode === "login" ? "Iniciar Sesión" : "Crear Cuenta"}
          </h2>
          <p className="text-sm text-muted-foreground mt-2 text-center">
            {mode === "login" 
              ? "Ingresa tus credenciales para continuar" 
              : "Regístrate para comenzar a usar la plataforma"}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <div className="flex flex-col gap-2">
            <Label htmlFor="email">Correo electrónico</Label>
            <Input 
              id="email"
              type="email" 
              placeholder="tu@correo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={errors.email ? "border-destructive focus-visible:ring-destructive/50" : ""}
            />
            {errors.email && <span className="text-xs text-destructive font-medium">{errors.email}</span>}
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor="password">Contraseña</Label>
            <Input 
              id="password"
              type="password" 
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={errors.password ? "border-destructive focus-visible:ring-destructive/50" : ""}
            />
            {errors.password && <span className="text-xs text-destructive font-medium">{errors.password}</span>}
          </div>

          {mode === "register" && (
            <div className="flex flex-col gap-2 animate-in fade-in slide-in-from-top-2 duration-300">
              <Label htmlFor="confirmPassword">Confirmar contraseña</Label>
              <Input 
                id="confirmPassword"
                type="password" 
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className={errors.confirmPassword ? "border-destructive focus-visible:ring-destructive/50" : ""}
              />
              {errors.confirmPassword && <span className="text-xs text-destructive font-medium">{errors.confirmPassword}</span>}
            </div>
          )}

          <Button type="submit" className="w-full mt-2 font-bold cursor-pointer">
            {mode === "login" ? "Entrar" : "Registrarse"}
          </Button>
        </form>

        <div className="mt-8 text-center text-sm">
          <span className="text-muted-foreground">
            {mode === "login" ? "¿No tienes una cuenta?" : "¿Ya tienes una cuenta?"}
          </span>{" "}
          <button 
            type="button"
            className="text-primary hover:underline font-bold cursor-pointer"
            onClick={() => {
              setMode(mode === "login" ? "register" : "login")
              setErrors({})
            }}
          >
            {mode === "login" ? "Regístrate aquí" : "Inicia sesión aquí"}
          </button>
        </div>
      </div>
    </div>
  )
}
