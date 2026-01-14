// =======================================================
// File: src/components/orgchart/useVirtualTree.ts
// =======================================================

import { useMemo } from 'react';
import type { OrgChartNode } from '../../services/employeeService';

export interface PositionedNode extends OrgChartNode {
  x: number;
  y: number;
  depth: number;
  subtreeWidth: number;
}

export interface Edge {
  fromId: string;
  toId: string;
  fromX: number;
  fromY: number;
  toX: number;
  toY: number;
}

export interface VirtualizedResult {
  nodes: PositionedNode[];
  edges: Edge[];
  visibleNodes: PositionedNode[];
  visibleEdges: Edge[];
  width: number;
  height: number;
  totalHeight: number;
}

const NODE_WIDTH = 200;
const NODE_HEIGHT = 65;
const HORIZONTAL_GAP = 12;
const VERTICAL_GAP = 40;
const OUTER_PADDING_X = 20;
const OUTER_PADDING_Y = 20;

function getId(node: OrgChartNode): string {
  return String(node.id);
}

function getVisibleChildren(node: OrgChartNode, expanded: Set<string>): OrgChartNode[] {
  if (!node.children?.length) return [];
  const id = getId(node);
  if (!expanded.has(id)) return [];
  return node.children;
}

export function useVirtualTree(
  tree: OrgChartNode[],
  expanded: Set<string>,
  containerHeight: number = 600,
  scrollTop: number = 0
): VirtualizedResult {
  const layout = useMemo(() => {
    const widths = new Map<string, number>();

    // Calculate the total width needed for a node's subtree
    // Level 5 (depth 4) uses vertical layout for its children (Level 6), so width is just one card
    const computeSubtreeWidth = (node: OrgChartNode, depth: number = 0): number => {
      const id = getId(node);
      const cached = widths.get(id);
      if (cached !== undefined) return cached;

      const children = getVisibleChildren(node, expanded);
      if (!children.length) {
        widths.set(id, NODE_WIDTH);
        return NODE_WIDTH;
      }

      // If this is Level 5 (depth 4), its children (Level 6) will be vertical
      // So the subtree width is just the width of this node (plus maybe padding if we wanted)
      if (depth === 4) {
        widths.set(id, NODE_WIDTH);
        return NODE_WIDTH;
      }

      // Levels 1-4
      // Check if we should split into multiple lines (count > 5) to improve readability
      if (children.length > 5 && depth < 4) {
        const mid = Math.ceil(children.length / 2);
        const row1 = children.slice(0, mid);
        const row2 = children.slice(mid);

        let w1 = 0;
        for (let i = 0; i < row1.length; i++) {
          w1 += computeSubtreeWidth(row1[i], depth + 1);
          if (i < row1.length - 1) w1 += HORIZONTAL_GAP;
        }

        let w2 = 0;
        for (let i = 0; i < row2.length; i++) {
          w2 += computeSubtreeWidth(row2[i], depth + 1);
          if (i < row2.length - 1) w2 += HORIZONTAL_GAP;
        }

        const finalWidth = Math.max(NODE_WIDTH, Math.max(w1, w2));
        widths.set(id, finalWidth);
        return finalWidth;
      }

      // Standard horizontal tree layout (<= 5 children)
      let sum = 0;
      for (let i = 0; i < children.length; i += 1) {
        const w = computeSubtreeWidth(children[i], depth + 1);
        sum += w;
        if (i < children.length - 1) sum += HORIZONTAL_GAP;
      }

      const finalWidth = Math.max(NODE_WIDTH, sum);
      widths.set(id, finalWidth);
      return finalWidth;
    };

    const nodes: PositionedNode[] = [];
    const edges: Edge[] = [];

    let maxX = 0;
    let maxY = 0;

    // Place a node and its children recursively
    const placeNode = (node: OrgChartNode, leftBound: number, depth: number, rowY: number): { node: PositionedNode, bottom: number } => {
      const id = getId(node);
      const subtreeWidth = widths.get(id) || NODE_WIDTH;

      // Center the node within its subtree width
      const x = leftBound + (subtreeWidth - NODE_WIDTH) / 2;
      const y = rowY;

      const positioned: PositionedNode = {
        ...node,
        x,
        y,
        depth,
        subtreeWidth,
      };

      nodes.push(positioned);

      // Calculate local bottom using actual placed children
      let localBottom = y + NODE_HEIGHT;

      const children = getVisibleChildren(node, expanded);
      if (children.length) {
        // Level 5 (depth 4): children are Level 6 -> vertical list layout
        if (depth === 4) {
          let childY = y + NODE_HEIGHT + VERTICAL_GAP;
          const childX = x; // Same X as parent (vertically aligned)

          for (const child of children) {
            const result = placeNode(child, childX, depth + 1, childY);
            localBottom = Math.max(localBottom, result.bottom);

            // Create edge
            edges.push({
              fromId: id,
              toId: getId(child),
              fromX: x + NODE_WIDTH / 2,
              fromY: y + NODE_HEIGHT,
              toX: result.node.x + NODE_WIDTH / 2,
              toY: result.node.y,
            });

            childY += NODE_HEIGHT + VERTICAL_GAP;
          }
        }
        // Levels 1-4 with > 5 children: Multi-line grid layout
        else if (children.length > 5 && depth < 4) {
          const mid = Math.ceil(children.length / 2);
          const row1 = children.slice(0, mid);
          const row2 = children.slice(mid);

          // Calculate Row 1 width
          let w1 = 0;
          row1.forEach((c, i) => {
            w1 += widths.get(getId(c)) || NODE_WIDTH;
            if (i < row1.length - 1) w1 += HORIZONTAL_GAP;
          });

          // Place Row 1
          let r1X = leftBound + (subtreeWidth - w1) / 2;
          let r1Y = y + NODE_HEIGHT + VERTICAL_GAP;
          let r1Bottom = r1Y;

          for (const child of row1) {
            const childWidth = widths.get(getId(child)) || NODE_WIDTH;
            const result = placeNode(child, r1X, depth + 1, r1Y);
            r1Bottom = Math.max(r1Bottom, result.bottom);

            edges.push({
              fromId: id,
              toId: getId(child),
              fromX: x + NODE_WIDTH / 2,
              fromY: y + NODE_HEIGHT,
              toX: result.node.x + NODE_WIDTH / 2,
              toY: result.node.y,
            });

            r1X += childWidth + HORIZONTAL_GAP;
          }

          // Place Row 2 (below Row 1's bottom)
          // Calculate Row 2 width
          let w2 = 0;
          row2.forEach((c, i) => {
            w2 += widths.get(getId(c)) || NODE_WIDTH;
            if (i < row2.length - 1) w2 += HORIZONTAL_GAP;
          });

          let r2X = leftBound + (subtreeWidth - w2) / 2;
          let r2Y = r1Bottom + VERTICAL_GAP;

          for (const child of row2) {
            const childWidth = widths.get(getId(child)) || NODE_WIDTH;
            const result = placeNode(child, r2X, depth + 1, r2Y);
            localBottom = Math.max(localBottom, result.bottom);

            // Edge from Parent -> Row 2 child
            // Note: This draws a long line crossing Row 1. Ideally we route around, but direct line is standard.
            edges.push({
              fromId: id,
              toId: getId(child),
              fromX: x + NODE_WIDTH / 2,
              fromY: y + NODE_HEIGHT,
              toX: result.node.x + NODE_WIDTH / 2,
              toY: result.node.y,
            });

            r2X += childWidth + HORIZONTAL_GAP;
          }
        }
        else {
          // Levels 1-4 standard: horizontal tree layout
          const childY = y + NODE_HEIGHT + VERTICAL_GAP;
          let childX = leftBound;

          for (const child of children) {
            const childWidth = widths.get(getId(child)) || NODE_WIDTH;
            const result = placeNode(child, childX, depth + 1, childY);
            localBottom = Math.max(localBottom, result.bottom);

            edges.push({
              fromId: id,
              toId: getId(child),
              fromX: x + NODE_WIDTH / 2,
              fromY: y + NODE_HEIGHT,
              toX: result.node.x + NODE_WIDTH / 2,
              toY: result.node.y,
            });

            childX += childWidth + HORIZONTAL_GAP;
          }
        }
      }

      // Update global max dims
      maxX = Math.max(maxX, leftBound + subtreeWidth);
      maxY = Math.max(maxY, localBottom);

      return { node: positioned, bottom: localBottom };
    };

    // First pass: compute all subtree widths
    for (const root of tree) {
      computeSubtreeWidth(root, 0); // Start at depth 0
    }

    // Second pass: place all nodes
    let rootX = OUTER_PADDING_X;
    const rootY = OUTER_PADDING_Y;

    for (const root of tree) {
      const rootWidth = widths.get(getId(root)) || NODE_WIDTH;
      placeNode(root, rootX, 0, rootY);
      rootX += rootWidth + HORIZONTAL_GAP * 2;
    }

    const width = Math.max(maxX + OUTER_PADDING_X, 800);
    const height = Math.max(maxY + OUTER_PADDING_Y, 600);

    return { nodes, edges, width, height };
  }, [tree, expanded]);

  const visibleNodes = useMemo(() => {
    const buffer = 400;
    const viewportStart = scrollTop - buffer;
    const viewportEnd = scrollTop + containerHeight + buffer;

    return layout.nodes.filter((n) => {
      const top = n.y;
      const bottom = n.y + NODE_HEIGHT;
      return bottom >= viewportStart && top <= viewportEnd;
    });
  }, [layout.nodes, scrollTop, containerHeight]);

  const visibleEdges = useMemo(() => {
    const visibleIds = new Set(visibleNodes.map((n) => String(n.id)));
    return layout.edges.filter((e) => visibleIds.has(e.fromId) || visibleIds.has(e.toId));
  }, [layout.edges, visibleNodes]);

  return {
    nodes: layout.nodes,
    edges: layout.edges,
    visibleNodes,
    visibleEdges,
    width: layout.width,
    height: layout.height,
    totalHeight: layout.height,
  };
}
