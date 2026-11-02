/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ViewButton } from "@web/views/view_button/view_button";

patch(ViewButton.prototype, {
    setup() {
        super.setup();

        const handleViewButton = this.handleViewButton;
        this.handleViewButton = async (...args) => {
            const hint = this._taskmasterHint;
            const result = this._taskmasterResult;
            if (!hint && !result) {
                return handleViewButton(...args);
            }

            hint?.classList.remove("d-none");
            result?.classList.add("d-none");

            let succeeded = false;
            try {
                const response = await handleViewButton(...args);
                succeeded = true;
                return response;
            } finally {
                hint?.classList.add("d-none");
                if (succeeded) {
                    result?.classList.remove("d-none");
                }
                this._taskmasterHint = null;
                this._taskmasterResult = null;
            }
        };
    },

    onClick(ev, newWindow) {
        this._taskmasterHint = null;
        this._taskmasterResult = null;

        const isTaskmasterRun =
            this.props.record?.resModel === "taskmaster.risk.wizard" &&
            this.clickParams.name === "action_run" &&
            !this.props.onClick;
        if (isTaskmasterRun) {
            const container = ev.target.closest(".modal") || document;
            this._taskmasterHint = container.querySelector(".o_taskmaster_run_hint");
            this._taskmasterResult = container.querySelector(".o_taskmaster_result");
        }

        return super.onClick(ev, newWindow);
    },
});
