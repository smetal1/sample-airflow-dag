import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.external_task_sensor import ExternalTaskMarker, ExternalTaskSensor

start_date = datetime.datetime(2015, 1, 1)

with DAG(
    dag_id="example_external_task_marker_parent",
    start_date=start_date,
    schedule_interval=None,
    tags=['example'],
) as parent_dag:
    # [START howto_operator_external_task_marker]
    parent_task = ExternalTaskMarker(task_id="parent_task",
                                     external_dag_id="example_external_task_marker_child",
                                     external_task_id="child_task1")
    # [END howto_operator_external_task_marker]

with DAG(
    dag_id="example_external_task_marker_child",
    start_date=start_date,
    schedule_interval=None,
    tags=['example'],
) as child_dag:
    # [START howto_operator_external_task_sensor]
    child_task1 = ExternalTaskSensor(task_id="child_task1",
                                     external_dag_id=parent_dag.dag_id,
                                     external_task_id=parent_task.task_id,
                                     mode="reschedule")
    # [END howto_operator_external_task_sensor]
    child_task2 = DummyOperator(task_id="child_task2")
    child_task1 >> child_task2
