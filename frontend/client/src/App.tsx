/* Sunlit Credential route map: public discovery, secure account entry, and RBAC workspaces are intentionally distinct yet visually continuous. */
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import { LanguageProvider } from "./contexts/LanguageContext";
import Home from "./pages/Home";
import { CareRoutesPage, FindCarePage, MarketplacePage, CommunityPage, ProfessionalsPage, StandardsPage, ToolsPage } from "./pages/PublicPages";
import { AuthPage } from "./pages/AuthPage";
import { VerifyEmailPage } from "./pages/VerifyEmailPage";
import Dashboard from "./pages/Dashboard";
import Onboarding from "./pages/Onboarding";
import { ScrollManager } from "./components/ScrollManager";

function Router(){return <Switch><Route path="/" component={Home}/><Route path="/find-care" component={FindCarePage}/><Route path="/clinics" component={FindCarePage}/><Route path="/care-routes" component={CareRoutesPage}/><Route path="/standards" component={StandardsPage}/><Route path="/marketplace" component={MarketplacePage}/><Route path="/community" component={CommunityPage}/><Route path="/professionals" component={ProfessionalsPage}/><Route path="/tools" component={ToolsPage}/><Route path="/feed-calculator" component={ToolsPage}/><Route path="/disease-support" component={ToolsPage}/><Route path="/login" component={()=> <AuthPage mode="login"/>}/><Route path="/register" component={()=> <AuthPage mode="register"/>}/><Route path="/verify-email" component={VerifyEmailPage}/><Route path="/onboarding" component={Onboarding}/><Route path="/portal/:module" component={Dashboard}/><Route path="/portal" component={Dashboard}/><Route component={NotFound}/></Switch>}
export default function App(){return <ErrorBoundary><ThemeProvider defaultTheme="light"><LanguageProvider><TooltipProvider><ScrollManager/><Router/><Toaster/></TooltipProvider></LanguageProvider></ThemeProvider></ErrorBoundary>}
