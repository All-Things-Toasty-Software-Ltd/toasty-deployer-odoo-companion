/** @odoo-module **/

import {Component, onWillStart, onWillUpdateProps, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class ToastyDeployerRunList extends Component {
    static template = "toasty_deployer.ToastyDeployerRunList";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");

        this.state = useState({
            runs: [],
            expandedRunId: null,
            loading: true,
        });

        onWillStart(() => this.loadRuns());
        onWillUpdateProps(() => this.loadRuns());
    }

    async loadRuns() {
        const resId = this.props.record?.resId;

        this.state.loading = true;

        try {
            const domain = resId ? [["repo_id", "=", resId]] : [];

            this.state.runs = await this.orm.searchRead(
                "toasty_deployer.run",
                domain,
                [
                    "id",
                    "name",
                    "commit_sha",
                    "status",
                    "exit_code",
                    "created_at",
                    "logs",
                ],
                {
                    order: "created_at desc",
                }
            );

            if (this.state.expandedRunId && !this.state.runs.some((run) => run.id === this.state.expandedRunId)) {
                this.state.expandedRunId = null;
            }
        } catch (error) {
            console.error("Toasty Deployer: Failed to load deployment runs", error);

            this.state.runs = [];
            this.state.expandedRunId = null;

            this.notification.add("Failed to load deployment runs.", {type: "danger",});
        } finally {
            this.state.loading = false;
        }
    }

    toggleLogs(runId, ev) {
        ev?.stopPropagation();

        this.state.expandedRunId = this.state.expandedRunId === runId ? null : runId;
    }

    isExpanded(runId) {
        return this.state.expandedRunId === runId;
    }

    getStatusBadgeClass(status) {
        switch (status) {
            case "success":
                return "text-bg-success";

            case "failure":
                return "text-bg-danger";

            case "running":
                return "text-bg-info";

            default:
                return "text-bg-secondary";
        }
    }

    getExitCodeClass(exitCode) {
        if (exitCode === null || exitCode === undefined) {
            return "text-muted";
        }

        return exitCode === 0 ? "text-success" : "text-danger";
    }
}

registry.category("view_widgets").add("toasty_deployer_run_list", {
    component: ToastyDeployerRunList,
});