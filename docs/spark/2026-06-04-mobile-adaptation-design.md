# Mobile Adaptation Design: FAB & RAG Upload Removal

## Goal
Adapt the mobile UI to prevent floating elements (Top Dock, Sidebar) from blocking the chat interface, and remove the file upload functionality from the RAG module to simplify the UI.

## Proposed Changes

### 1. Mobile FAB (Floating Action Button) Layout
- **Desktop**: The existing Top Dock will remain visible (`md:flex max-md:hidden`).
- **Mobile**: The Top Dock and the top-left history toggle button will be hidden on mobile devices. A new FAB will be introduced at `bottom-24 right-4` (`max-md:flex md:hidden`), sitting cleanly above the chat composer.
- **FAB Styling**: "Liquid Glass" effect. Frosted glass (`backdrop-blur-md`), semi-transparent background (`bg-black/40`), inner border (`border-white/10`), and a subtle shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1),0_8px_30px_rgba(0,0,0,0.12)]`).
- **FAB Interaction**: Clicking the FAB will expand a staggered vertical list of action buttons (Home, RAG, Agent, History). The FAB icon itself will rotate into a close icon ('X') using a smooth CSS or Framer Motion spring animation.

### 2. History Sidebar Integration
- The "History" button in the FAB menu will toggle the existing `FloatingSidebar`.
- To prevent occlusion on mobile, when the sidebar is open, a semi-transparent backdrop should cover the screen, allowing users to dismiss the sidebar by clicking the backdrop. (This ensures focus remains solely on the history selection).

### 3. RAG Module Simplification
- **`HikingRAG.tsx`**: Remove the hidden `<input type="file" />` element, the `fileInputRef`, and the `handleFileUpload` function.
- **`GeminiThread` instantiation**: Remove the `onUploadClick` prop from `<GeminiThread>` in the RAG module. This will natively hide the paperclip icon and shift the input box to the left.

## Verification
- Resize the browser to a mobile width (< 768px) and verify the Top Dock hides and the FAB appears.
- Ensure clicking the FAB smoothly reveals the module options and history toggle.
- Verify that opening the history sidebar provides a clear, un-occluded view with a dismissible backdrop.
- Verify that the RAG chat input no longer displays the paperclip upload icon.
