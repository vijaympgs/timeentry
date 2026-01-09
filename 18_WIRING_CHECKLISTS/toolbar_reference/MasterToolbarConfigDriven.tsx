import React, { useEffect, useCallback } from "react";
import {
    Plus, Edit, Save, X, RotateCcw,
    CheckCircle, Send, Ban, FileEdit,
    Eye, Printer, Mail,
    ChevronFirst, ChevronLeft, ChevronRight, ChevronLast,
    RefreshCw, Trash2, PauseCircle, Octagon,
    Search, Filter,
    Upload, Download, Copy,
    StickyNote, Paperclip, Settings, HelpCircle, LogOut
} from "lucide-react";
import { useToolbarConfig } from "../../../../../src/hooks/useToolbarConfig";

/**
 * MASTER TOOLBAR REPRODUCIBLE COMPONENT
 * ------------------------------------
 * This component is the GOLD STANDARD for all ERP modules (Retail, HRM, CRM, FMS).
 * It is backend-driven, meaning the permissions and visible buttons are controlled
 * by a character-string configuration (e.g., "NRQFX") fetched via useToolbarConfig.
 */

export type MasterMode = "VIEW" | "EDIT" | "CREATE";

interface MasterToolbarProps {
    viewId: string; // Must match ERPMenuItem.menu_id in database
    mode: MasterMode;
    onAction: (action: string) => void;
    hasSelection?: boolean;
}

interface ActionButton {
    id: string;
    icon: React.ElementType;
    label: string;
    shortcut: string;
    group: number;
    shortcutLabel: string;
    colorClass: string;
    permissionKey: keyof import("../../../../../src/hooks/useToolbarConfig").ToolbarPermissions;
}

const ACTIONS: ActionButton[] = [
    // Group 1: CRUD Operations
    { id: 'new', icon: Plus, label: 'New', shortcut: 'f2', group: 1, shortcutLabel: 'F2', colorClass: 'text-blue-600', permissionKey: 'new' },
    { id: 'edit', icon: Edit, label: 'Edit', shortcut: 'f3', group: 1, shortcutLabel: 'F3', colorClass: 'text-blue-600', permissionKey: 'edit' },
    { id: 'save', icon: Save, label: 'Save', shortcut: 'f8', group: 1, shortcutLabel: 'F8', colorClass: 'text-emerald-600', permissionKey: 'save' },
    { id: 'cancel', icon: X, label: 'Cancel', shortcut: 'esc', group: 1, shortcutLabel: 'ESC', colorClass: 'text-gray-600', permissionKey: 'cancel' },
    { id: 'clear', icon: RotateCcw, label: 'Clear', shortcut: 'f5', group: 1, shortcutLabel: 'F5', colorClass: 'text-amber-500', permissionKey: 'clear' },

    // Group 2: Workflow / Approval
    { id: 'authorize', icon: CheckCircle, label: 'Authorize', shortcut: 'f10', group: 2, shortcutLabel: 'F10', colorClass: 'text-green-600', permissionKey: 'authorize' },
    { id: 'submit', icon: Send, label: 'Submit', shortcut: 'alt+s', group: 2, shortcutLabel: 'Alt+S', colorClass: 'text-blue-600', permissionKey: 'submit' },
    { id: 'reject', icon: Ban, label: 'Reject', shortcut: 'alt+r', group: 2, shortcutLabel: 'Alt+R', colorClass: 'text-red-500', permissionKey: 'reject' },
    { id: 'amend', icon: FileEdit, label: 'Amend', shortcut: 'alt+a', group: 2, shortcutLabel: 'Alt+A', colorClass: 'text-orange-600', permissionKey: 'amend' },

    // Group 3: View & Print
    { id: 'view', icon: Eye, label: 'View', shortcut: 'f7', group: 3, shortcutLabel: 'F7', colorClass: 'text-indigo-600', permissionKey: 'view' },
    { id: 'print', icon: Printer, label: 'Print', shortcut: 'ctrl+p', group: 3, shortcutLabel: 'Ctrl+P', colorClass: 'text-purple-600', permissionKey: 'print' },
    { id: 'email', icon: Mail, label: 'Email', shortcut: 'ctrl+e', group: 3, shortcutLabel: 'Ctrl+E', colorClass: 'text-sky-600', permissionKey: 'email' },

    // Group 4: Navigation
    { id: 'first', icon: ChevronFirst, label: 'First', shortcut: 'home', group: 4, shortcutLabel: 'Home', colorClass: 'text-gray-600', permissionKey: 'first' },
    { id: 'prev', icon: ChevronLeft, label: 'Previous', shortcut: 'pageup', group: 4, shortcutLabel: 'PgUp', colorClass: 'text-gray-600', permissionKey: 'prev' },
    { id: 'next', icon: ChevronRight, label: 'Next', shortcut: 'pagedown', group: 4, shortcutLabel: 'PgDn', colorClass: 'text-gray-600', permissionKey: 'next' },
    { id: 'last', icon: ChevronLast, label: 'Last', shortcut: 'end', group: 4, shortcutLabel: 'End', colorClass: 'text-gray-600', permissionKey: 'last' },

    // Group 5: Data Ops
    { id: 'refresh', icon: RefreshCw, label: 'Refresh', shortcut: 'f9', group: 5, shortcutLabel: 'F9', colorClass: 'text-cyan-600', permissionKey: 'refresh' },
    { id: 'delete', icon: Trash2, label: 'Delete', shortcut: 'f4', group: 5, shortcutLabel: 'F4', colorClass: 'text-rose-600', permissionKey: 'delete' },
    { id: 'hold', icon: PauseCircle, label: 'Hold', shortcut: 'alt+h', group: 5, shortcutLabel: 'Alt+H', colorClass: 'text-yellow-600', permissionKey: 'hold' },
    { id: 'void', icon: Octagon, label: 'Void', shortcut: 'alt+v', group: 5, shortcutLabel: 'Alt+V', colorClass: 'text-red-700', permissionKey: 'void' },

    // Group 6: Search & Filter
    { id: 'search', icon: Search, label: 'Search', shortcut: 'ctrl+f', group: 6, shortcutLabel: 'Ctrl+F', colorClass: 'text-slate-600', permissionKey: 'search' },
    { id: 'filter', icon: Filter, label: 'Filter', shortcut: 'alt+f', group: 6, shortcutLabel: 'Alt+F', colorClass: 'text-slate-600', permissionKey: 'filter' },

    // Group 7: Import/Export
    { id: 'upload', icon: Upload, label: 'Import', shortcut: 'ctrl+i', group: 7, shortcutLabel: 'Ctrl+I', colorClass: 'text-violet-600', permissionKey: 'upload' },
    { id: 'download', icon: Download, label: 'Export', shortcut: 'ctrl+e', group: 7, shortcutLabel: 'Ctrl+E', colorClass: 'text-indigo-600', permissionKey: 'download' },
    { id: 'clone', icon: Copy, label: 'Clone', shortcut: 'ctrl+shift+c', group: 7, shortcutLabel: 'Ctrl+Shift+C', colorClass: 'text-blue-500', permissionKey: 'clone' },

    // Group 8: Tools
    { id: 'notes', icon: StickyNote, label: 'Notes', shortcut: 'alt+n', group: 8, shortcutLabel: 'Alt+N', colorClass: 'text-yellow-500', permissionKey: 'notes' },
    { id: 'attach', icon: Paperclip, label: 'Attach', shortcut: 'alt+u', group: 8, shortcutLabel: 'Alt+U', colorClass: 'text-gray-500', permissionKey: 'attach' },
    { id: 'settings', icon: Settings, label: 'Settings', shortcut: 'alt+o', group: 8, shortcutLabel: 'Alt+O', colorClass: 'text-gray-600', permissionKey: 'settings' },

    // Group 9: Help & Exit
    { id: 'help', icon: HelpCircle, label: 'Help', shortcut: 'f1', group: 9, shortcutLabel: 'F1', colorClass: 'text-blue-500', permissionKey: 'help' },
    { id: 'exit', icon: LogOut, label: 'Exit', shortcut: 'esc', group: 9, shortcutLabel: 'ESC', colorClass: 'text-gray-600', permissionKey: 'exit' },
];

export const MasterToolbar: React.FC<MasterToolbarProps> = ({
    viewId,
    mode,
    onAction,
    hasSelection = false
}) => {
    const { config, loading } = useToolbarConfig(viewId);

    const isActionDisabled = useCallback((action: ActionButton): boolean => {
        // 1. Loading guard
        if (!config) return action.id !== 'exit';

        // 2. Permission-based enable/disable (From character string logic in hook)
        if (!config.permissions[action.permissionKey]) return true;

        // 3. Mode-based state machine
        switch (mode) {
            case 'VIEW':
                // VIEW mode allows navigation, search, and workflow (status dependent)
                return !['new', 'edit', 'view', 'print', 'email', 'refresh', 'delete', 'exit', 'download', 'clone', 'upload', 'first', 'prev', 'next', 'last', 'search', 'filter', 'notes', 'attach', 'settings', 'help', 'submit', 'reject', 'authorize', 'hold', 'void', 'amend'].includes(action.id);
            case 'EDIT':
            case 'CREATE':
                // EDIT/CREATE only allows transactional actions
                return !['save', 'cancel', 'clear', 'help', 'notes', 'attach', 'settings'].includes(action.id);
            default:
                return false;
        }
    }, [mode, config]);

    const handleAction = useCallback((actionId: string) => {
        onAction(actionId);
    }, [onAction]);

    // Keyboard handling logic... (same as core)
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            const action = ACTIONS.find(a => {
                const parts = a.shortcut.split('+');
                return parts.every(part => {
                    if (part === 'ctrl') return e.ctrlKey;
                    if (part === 'alt') return e.altKey;
                    if (part === 'shift') return e.shiftKey;
                    return e.key.toLowerCase() === part.toLowerCase();
                });
            });

            if (action && !isActionDisabled(action)) {
                e.preventDefault();
                handleAction(action.id);
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [handleAction, isActionDisabled]);

    if (loading) return <div className="toolbar-loading">Loading...</div>;

    let currentGroup = 0;
    return (
        <div className="toolbar-container h-[42px] bg-[#f3f2f1] border-b border-[#d1d1d1] flex items-center gap-1 px-4 shadow-sm">
            {ACTIONS.map((action) => {
                const disabled = isActionDisabled(action);
                const showSeparator = action.group !== currentGroup && currentGroup !== 0;
                currentGroup = action.group;

                return (
                    <React.Fragment key={action.id}>
                        {showSeparator && <div className="h-6 w-px bg-gray-300 mx-1" />}
                        <button
                            onClick={() => handleAction(action.id)}
                            disabled={disabled}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded transition-all text-xs font-medium 
                                ${disabled ? 'opacity-40 cursor-not-allowed' : 'hover:bg-white hover:shadow-sm active:scale-95'}`}
                            title={`${action.label} (${action.shortcutLabel})`}
                        >
                            <action.icon className={`w-4 h-4 ${disabled ? 'text-gray-400' : action.colorClass}`} />
                            <span className={disabled ? 'text-gray-400' : 'text-gray-700'}>{action.label}</span>
                        </button>
                    </React.Fragment>
                );
            })}
        </div>
    );
};
