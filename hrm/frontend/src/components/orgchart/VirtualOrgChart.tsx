// =======================================================
// File: src/components/orgchart/VirtualOrgChart.tsx
// =======================================================

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronDown, ChevronRight, Search, User, ZoomIn, ZoomOut, RotateCcw, Filter, Maximize2, Minimize2, Download } from 'lucide-react';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import { employeeService, type OrgChartNode } from '../../services/employeeService';
import { useVirtualTree, type PositionedNode } from './useVirtualTree';
import './orgChart.virtual.css';

function nodeId(n: OrgChartNode): string {
  return String(n.id);
}

function collectIds(nodes: OrgChartNode[], out: Set<string>) {
  for (const n of nodes) {
    out.add(nodeId(n));
    if (n.children?.length) collectIds(n.children, out);
  }
}

function findNodeById(nodes: OrgChartNode[], id: string): OrgChartNode | null {
  for (const n of nodes) {
    if (nodeId(n) === id) return n;
    if (n.children?.length) {
      const hit = findNodeById(n.children, id);
      if (hit) return hit;
    }
  }
  return null;
}

function isDescendant(root: OrgChartNode, targetId: string): boolean {
  if (!root.children?.length) return false;
  for (const c of root.children) {
    const cid = nodeId(c);
    if (cid === targetId) return true;
    if (isDescendant(c, targetId)) return true;
  }
  return false;
}

function initials(fullName: string): string {
  const parts = fullName.trim().split(/\s+/).filter(Boolean);
  if (!parts.length) return 'NA';
  const a = parts[0]?.[0] ?? 'N';
  const b = parts.length > 1 ? (parts[parts.length - 1]?.[0] ?? 'A') : (parts[0]?.[1] ?? 'A');
  return `${a}${b}`.toUpperCase();
}

function filterTree(nodes: OrgChartNode[], term: string): OrgChartNode[] {
  const q = term.trim().toLowerCase();
  if (!q) return nodes;

  const matches = (n: OrgChartNode) => {
    const blob = [
      n.full_name,
      n.first_name,
      n.last_name,
      n.position_title,
      n.department_name,
      n.employee_number,
      n.work_email,
      n.manager_name,
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();
    return blob.includes(q);
  };

  const walk = (list: OrgChartNode[]): OrgChartNode[] => {
    const out: OrgChartNode[] = [];
    for (const n of list) {
      const kids = n.children?.length ? walk(n.children) : [];
      if (matches(n) || kids.length) {
        out.push({
          ...n,
          children: kids,
        });
      }
    }
    return out;
  };

  return walk(nodes);
}

const VirtualOrgChart: React.FC = () => {
  const [roots, setRoots] = useState<OrgChartNode[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [draggingId, setDraggingId] = useState<string | null>(null);
  const [hoverId, setHoverId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isExporting, setIsExporting] = useState(false);

  // Zoom and filter states
  const [zoom, setZoom] = useState(1); // Default to 100% zoom
  const [selectedDepartment, setSelectedDepartment] = useState<string>('');
  const [maxLevel, setMaxLevel] = useState<number | null>(null);

  const viewportRef = useRef<HTMLDivElement>(null);
  const [containerHeight, setContainerHeight] = useState(600);
  const [scrollTop, setScrollTop] = useState(0);

  const load = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await employeeService.getHierarchy();
      const tree = Array.isArray(res?.hierarchy) ? res.hierarchy : [];
      setRoots(tree);

      const all = new Set<string>();
      collectIds(tree, all);
      setExpanded(all);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load org chart');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    if (!viewportRef.current) return;
    const el = viewportRef.current;

    const apply = () => setContainerHeight(el.clientHeight || 600);
    apply();

    const ro = new ResizeObserver(() => apply());
    ro.observe(el);

    return () => ro.disconnect();
  }, []);

  // Extract unique departments
  const departments = useMemo(() => {
    const depts = new Set<string>();
    const extractDepts = (nodes: OrgChartNode[]) => {
      for (const n of nodes) {
        if (n.department_name) depts.add(n.department_name);
        if (n.children?.length) extractDepts(n.children);
      }
    };
    extractDepts(roots);
    return Array.from(depts).sort();
  }, [roots]);

  // Apply search filter
  const searchFilteredRoots = useMemo(() => filterTree(roots, searchTerm), [roots, searchTerm]);

  // Apply department and level filters
  const filteredRoots = useMemo(() => {
    let result = searchFilteredRoots;

    // Filter by department
    if (selectedDepartment) {
      const filterByDept = (nodes: OrgChartNode[]): OrgChartNode[] => {
        const out: OrgChartNode[] = [];
        for (const n of nodes) {
          const kids = n.children?.length ? filterByDept(n.children) : [];
          if (n.department_name === selectedDepartment || kids.length) {
            out.push({ ...n, children: kids });
          }
        }
        return out;
      };
      result = filterByDept(result);
    }

    // Filter by max level
    if (maxLevel !== null) {
      const filterByLevel = (nodes: OrgChartNode[], currentLevel: number): OrgChartNode[] => {
        if (currentLevel >= maxLevel) return [];
        return nodes.map(n => ({
          ...n,
          children: n.children?.length && currentLevel < maxLevel
            ? filterByLevel(n.children, currentLevel + 1)
            : []
        }));
      };
      result = filterByLevel(result, 0); // Start at 0 (root is level 1)
    }

    return result;
  }, [searchFilteredRoots, selectedDepartment, maxLevel]);

  useEffect(() => {
    const q = searchTerm.trim();
    if (!q) return;
    const all = new Set<string>();
    collectIds(filteredRoots, all);
    setExpanded(all);
  }, [searchTerm, filteredRoots]);

  const toggle = useCallback((id: string) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  // Zoom controls
  const handleZoomIn = useCallback(() => {
    setZoom(prev => Math.min(prev + 0.1, 2));
  }, []);

  const handleZoomOut = useCallback(() => {
    setZoom(prev => Math.max(prev - 0.1, 0.1));
  }, []);

  const handleZoomReset = useCallback(() => {
    setZoom(1);
  }, []);

  // Expand/Collapse all
  const handleExpandAll = useCallback(() => {
    const all = new Set<string>();
    collectIds(roots, all); // Use roots, not filteredRoots
    setExpanded(all);
  }, [roots]);

  const handleCollapseAll = useCallback(() => {
    setExpanded(new Set());
  }, []);

  const handleExportPDF = useCallback(async () => {
    setIsExporting(true);
    // Allow React to render the full tree
    await new Promise(resolve => setTimeout(resolve, 500));

    try {
      // Find the inner container that holds the scalable content
      // We target the div with position relative inside viewport
      const viewport = viewportRef.current;
      if (!viewport) throw new Error('Viewport not found');

      const content = viewport.firstChild as HTMLElement;
      if (!content) throw new Error('Content not found');

      const canvas = await html2canvas(content, {
        scale: 2, // Higher quality
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
        // Ensure we capture full dimensions even if scrolled
        windowWidth: content.scrollWidth,
        windowHeight: content.scrollHeight,
        width: content.scrollWidth,
        height: content.scrollHeight,
        x: 0,
        y: 0
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: content.scrollWidth > content.scrollHeight ? 'landscape' : 'portrait',
        unit: 'px',
        format: [content.scrollWidth, content.scrollHeight]
      });

      pdf.addImage(imgData, 'PNG', 0, 0, content.scrollWidth, content.scrollHeight);
      pdf.save('organizational-chart.pdf');
    } catch (err) {
      console.error('Export PDF failed:', err);
      setError('Failed to generate PDF');
    } finally {
      setIsExporting(false);
    }
  }, []);

  // Auto-expand all on initial load
  useEffect(() => {
    if (roots.length > 0 && expanded.size === 0) {
      const all = new Set<string>();
      collectIds(roots, all);
      setExpanded(all);
    }
  }, [roots]);

  const onScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);

  // Drag-to-scroll functionality
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [scrollStart, setScrollStart] = useState({ x: 0, y: 0 });

  const handleMouseDown = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    // Only start drag if clicking on the viewport background, not on cards
    if ((e.target as HTMLElement).classList.contains('org-viewport') ||
      (e.target as HTMLElement).classList.contains('org-chart-wrapper')) {
      setIsDragging(true);
      setDragStart({ x: e.clientX, y: e.clientY });
      if (viewportRef.current) {
        setScrollStart({
          x: viewportRef.current.scrollLeft,
          y: viewportRef.current.scrollTop
        });
      }
      e.preventDefault();
    }
  }, []);

  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    if (!isDragging || !viewportRef.current) return;

    const dx = e.clientX - dragStart.x;
    const dy = e.clientY - dragStart.y;

    viewportRef.current.scrollLeft = scrollStart.x - dx;
    viewportRef.current.scrollTop = scrollStart.y - dy;
  }, [isDragging, dragStart, scrollStart]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleMouseLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const layout = useVirtualTree(
    filteredRoots,
    expanded,
    containerHeight / zoom,
    scrollTop / zoom
  );

  const handleDragStart = useCallback((e: React.DragEvent, id: string) => {
    setDraggingId(id);
    setHoverId(null);
    e.dataTransfer.setData('text/plain', id);
    e.dataTransfer.effectAllowed = 'move';
  }, []);

  const handleDragEnd = useCallback(() => {
    setDraggingId(null);
    setHoverId(null);
  }, []);

  const handleDragOver = useCallback(
    (e: React.DragEvent, id: string) => {
      if (!draggingId) return;
      if (draggingId === id) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      setHoverId(id);
    },
    [draggingId]
  );

  const handleDrop = useCallback(
    async (e: React.DragEvent, targetId: string) => {
      e.preventDefault();

      const draggedId = e.dataTransfer.getData('text/plain') || draggingId;
      setHoverId(null);

      if (!draggedId) return;
      if (draggedId === targetId) return;

      const draggedNode = findNodeById(roots, draggedId);
      if (!draggedNode) return;
      if (isDescendant(draggedNode, targetId)) return;

      try {
        await employeeService.updateManager(draggedId, targetId);
        await load();
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to update manager');
      } finally {
        setDraggingId(null);
        setHoverId(null);
      }
    },
    [draggingId, roots, load]
  );

  const renderNode = useCallback(
    (node: PositionedNode, isFirstAtLevel: boolean = false) => {
      const id = nodeId(node);
      const hasChildren = !!node.children?.length;
      const open = expanded.has(id);
      const fullName = node.full_name || `${node.first_name} ${node.last_name}`.trim();

      return (
        <div
          key={id}
          className={['org-node', draggingId === id ? 'dragging' : '', hoverId === id ? 'drop-target' : '']
            .filter(Boolean)
            .join(' ')}
          style={{ left: `${node.x}px`, top: `${node.y}px` }}
          draggable
          onDragStart={(e) => handleDragStart(e, id)}
          onDragEnd={handleDragEnd}
          onDragOver={(e) => handleDragOver(e, id)}
          onDrop={(e) => void handleDrop(e, id)}
        >
          {/* Level label - only on first node of each level */}
          {isFirstAtLevel && (
            <div className="org-level-label">
              Level {node.depth + 1}
            </div>
          )}

          <div className="org-card">
            <div className="org-avatar">
              {fullName ? initials(fullName) : <User size={16} />}
            </div>
            <div className="org-info">
              <div className="org-name">{fullName || '—'}</div>
              <div className="org-title">
                {[node.position_title, node.department_name].filter(Boolean).join(' • ') || '—'}
              </div>
              <div className="org-meta">
                {node.employee_number || ''}
              </div>
            </div>

            {hasChildren && (
              <button
                type="button"
                className="org-toggle"
                onClick={(e) => {
                  e.stopPropagation();
                  toggle(id);
                }}
                aria-label={open ? 'Collapse' : 'Expand'}
              >
                {open ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
              </button>
            )}
          </div>
        </div>
      );
    },
    [draggingId, hoverId, expanded, handleDragStart, handleDragEnd, handleDragOver, handleDrop, toggle]
  );

  const renderConnections = useCallback(() => {
    if (!layout.edges.length) return null;

    return (
      <svg
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: layout.width,
          height: layout.height,
          pointerEvents: 'none',
        }}
      >
        {layout.edges.map((edge, idx) => {
          const midY = edge.fromY + (edge.toY - edge.fromY) / 2;

          // Create a smooth curved path
          const path = `
            M ${edge.fromX} ${edge.fromY}
            L ${edge.fromX} ${midY}
            L ${edge.toX} ${midY}
            L ${edge.toX} ${edge.toY}
          `;

          return (
            <path
              key={`${edge.fromId}-${edge.toId}-${idx}`}
              d={path}
              className="org-connector"
            />
          );
        })}
      </svg>
    );
  }, [layout.edges, layout.width, layout.height]);

  if (isLoading) {
    return (
      <div style={{
        padding: 48,
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 16
      }}>
        <div style={{
          width: 48,
          height: 48,
          border: '4px solid #e2e8f0',
          borderTop: '4px solid #667eea',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <div style={{ fontSize: 16, color: '#64748b', fontWeight: 600 }}>Loading organization chart...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        padding: 48,
        textAlign: 'center',
        color: '#dc2626',
        background: '#fef2f2',
        border: '1px solid #fecaca',
        borderRadius: 12,
        margin: 20
      }}>
        <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>Error</div>
        <div>{error}</div>
      </div>
    );
  }

  return (
    <div className="org-chart-wrapper">
      <div className="org-toolbar">
        <div className="org-search-wrapper">
          <div className="org-search-icon">
            <Search size={18} />
          </div>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search employees, departments..."
            className="org-search-input"
          />
        </div>

        {/* Department Filter */}
        <select
          value={selectedDepartment}
          onChange={(e) => setSelectedDepartment(e.target.value)}
          className="org-select"
          style={{
            padding: '10px 12px',
            borderRadius: '10px',
            border: '1.5px solid #e2e8f0',
            background: '#f8fafc',
            fontSize: '14px',
            fontWeight: 600,
            color: '#475569',
            cursor: 'pointer',
            minWidth: '160px'
          }}
        >
          <option value="">All Departments</option>
          {departments.map(dept => (
            <option key={dept} value={dept}>{dept}</option>
          ))}
        </select>

        {/* Level Filter */}
        <select
          value={maxLevel === null ? '' : maxLevel}
          onChange={(e) => setMaxLevel(e.target.value ? parseInt(e.target.value) : null)}
          className="org-select"
          style={{
            padding: '10px 12px',
            borderRadius: '10px',
            border: '1.5px solid #e2e8f0',
            background: '#f8fafc',
            fontSize: '14px',
            fontWeight: 600,
            color: '#475569',
            cursor: 'pointer',
            minWidth: '140px'
          }}
        >
          <option value="">All Levels</option>
          <option value="1">Level 1</option>
          <option value="2">Level 1-2</option>
          <option value="3">Level 1-3</option>
          <option value="4">Level 1-4</option>
          <option value="5">Level 1-5</option>
          <option value="6">Level 1-6</option>
        </select>

        {/* Zoom Controls */}
        <div style={{ display: 'flex', gap: '6px', alignItems: 'center', borderLeft: '1px solid #e2e8f0', paddingLeft: '12px', marginLeft: '6px' }}>
          <button
            type="button"
            onClick={handleZoomOut}
            className="org-button"
            title="Zoom Out"
            style={{ padding: '10px' }}
          >
            <ZoomOut size={18} />
          </button>

          <div style={{
            fontSize: '14px',
            fontWeight: 600,
            color: '#475569',
            minWidth: '50px',
            textAlign: 'center'
          }}>
            {Math.round(zoom * 100)}%
          </div>

          <button
            type="button"
            onClick={handleZoomIn}
            className="org-button"
            title="Zoom In"
            style={{ padding: '10px' }}
          >
            <ZoomIn size={18} />
          </button>

          <button
            type="button"
            onClick={handleZoomReset}
            className="org-button"
            title="Reset Zoom"
            style={{ padding: '10px' }}
          >
            <RotateCcw size={18} />
          </button>
        </div>

        {/* Expand/Collapse All */}
        <button
          type="button"
          onClick={handleExpandAll}
          className="org-button"
          title="Expand All"
        >
          <Maximize2 size={16} />
          <span>Expand All</span>
        </button>

        <button
          type="button"
          onClick={handleCollapseAll}
          className="org-button"
          title="Collapse All"
        >
          <Minimize2 size={16} />
          <span>Collapse All</span>
        </button>

        <button
          type="button"
          onClick={handleExportPDF}
          className="org-button"
          title="Export as PDF"
          disabled={isExporting}
        >
          <Download size={16} />
          <span>{isExporting ? 'Exporting...' : 'Export PDF'}</span>
        </button>

        <button
          type="button"
          onClick={() => void load()}
          className="org-button"
          style={{ marginLeft: 'auto' }}
        >
          Reload
        </button>
      </div>

      <div
        ref={viewportRef}
        className="org-viewport"
        onScroll={onScroll}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseLeave}
        style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
      >
        <div style={{
          width: `${layout.width * zoom}px`,
          height: `${layout.height * zoom}px`,
          position: 'relative'
        }}>
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: `${layout.width}px`,
              height: `${layout.height}px`,
              transform: `scale(${zoom})`,
              transformOrigin: 'top left',
            }}
          >
            {renderConnections()}
            {(() => {
              // Track first node at each depth level
              const firstAtLevel = new Set<number>();
              return (isExporting ? layout.nodes : layout.visibleNodes).map((n) => {
                const isFirst = !firstAtLevel.has(n.depth);
                if (isFirst) firstAtLevel.add(n.depth);
                return renderNode(n, isFirst);
              });
            })()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VirtualOrgChart;
